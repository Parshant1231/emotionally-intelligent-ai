# backend/app/services/bot_service.py

import sys
import os

# Add ml/ folder to path so we can import our bots
ML_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)
    )))),
    "ml"
)
sys.path.insert(0, ML_PATH)

from traditional_chatbot.bot import TraditionalChatbot
from ei_chatbot.bot import EIChatbot
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import ChatSession, ChatMessage
from datetime import datetime
import uuid


class BotService:
    """
    Singleton service that holds both bot instances.
    Bots are loaded ONCE at startup — not on every request.
    Loading them on every request would take 30+ seconds each time.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def initialize(self):
        """Load both models into memory. Called once at app startup."""
        if self._initialized:
            return
        print("🔄 Initializing both chatbots...")
        self.trad_sessions: dict[str, TraditionalChatbot] = {}
        self.ei_sessions:   dict[str, EIChatbot]          = {}
        self._initialized = True
        print("✅ BotService ready")

    def _get_or_create_bot(self, session_id: str, bot_type: str):
        """
        Get existing bot for this session or create a new one.
        Each user session gets its own bot instance with its own history.
        """
        if bot_type == "traditional":
            if session_id not in self.trad_sessions:
                self.trad_sessions[session_id] = TraditionalChatbot()
            return self.trad_sessions[session_id]

        elif bot_type == "ei":
            if session_id not in self.ei_sessions:
                self.ei_sessions[session_id] = EIChatbot()
            return self.ei_sessions[session_id]

        else:
            raise ValueError(f"Invalid bot_type: {bot_type}. Use 'ei' or 'traditional'")

    async def chat(
        self,
        session_id: str,
        user_input: str,
        bot_type: str,
        db: AsyncSession
    ) -> dict:
        """
        Main chat method — handles message, saves to DB, returns response.
        """
        bot = self._get_or_create_bot(session_id, bot_type)
        result = bot.respond(user_input)

        # Get current turn count for this session from DB
        turn_number = result["turn"]

        # Save user message to DB
        user_msg = ChatMessage(
            session_id         = session_id,
            turn_number        = turn_number,
            role               = "user",
            content            = user_input,
            detected_emotion   = result.get("detected_emotion"),
            emotion_confidence = result.get("emotion_confidence"),
            emotion_scores     = result.get("emotion_scores"),
            style_applied      = result.get("style_applied"),
            bot_type           = bot_type,
        )
        db.add(user_msg)

        # Save bot response to DB
        bot_msg = ChatMessage(
            session_id  = session_id,
            turn_number = turn_number,
            role        = "bot",
            content     = result["response"],
            bot_type    = bot_type,
        )
        db.add(bot_msg)

        # Update session turn count
        session_record = await db.scalar(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        if session_record:
            session_record.turn_count = turn_number

        await db.commit()
        return result

    async def end_session(
        self,
        session_id: str,
        bot_type: str,
        satisfaction: float,
        db: AsyncSession
    ) -> dict:
        """
        Called when user submits satisfaction rating after chat.
        Saves rating + sentiment shift to DB — feeds OBJ 3 analysis.
        """
        # Get sentiment shift from EI bot's session log
        sentiment_shift = None
        if bot_type == "ei" and session_id in self.ei_sessions:
            ei_bot = self.ei_sessions[session_id]
            conv_data = ei_bot.emotion_detector.detect_conversation(
                [{"role": "user", "content": log["user_input"]}
                 for log in ei_bot.session_log]
            )
            sentiment_shift = conv_data.get("sentiment_shift")

        # Update session record
        session_record = await db.scalar(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        if session_record:
            session_record.satisfaction    = satisfaction
            session_record.sentiment_shift = sentiment_shift
            session_record.ended_at        = datetime.utcnow()
            await db.commit()

        # Clean up bot instance from memory
        if bot_type == "traditional" and session_id in self.trad_sessions:
            del self.trad_sessions[session_id]
        elif bot_type == "ei" and session_id in self.ei_sessions:
            del self.ei_sessions[session_id]

        return {
            "session_id":     session_id,
            "satisfaction":   satisfaction,
            "sentiment_shift": sentiment_shift,
            "status":         "session_ended"
        }


# Global singleton instance
bot_service = BotService()