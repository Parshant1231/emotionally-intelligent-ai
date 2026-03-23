# ml/ei_chatbot/bot.py

import sys
import os

# Add project root to path so we can import EmotionDetector
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from emotion_detector.detector import EmotionDetector

# -------------------------------------------------------------------
# This is the core "emotional intelligence" layer.
# Each emotion maps to a response STYLE modifier.
# The bot doesn't just respond — it responds with appropriate tone.
# This is what differentiates it from the traditional bot.
# -------------------------------------------------------------------
EMOTION_STYLE = {
    "joy": {
        "prefix": "That's wonderful to hear! ",
        "style": "enthusiastic and warm"
    },
    "sadness": {
        "prefix": "I'm sorry you're feeling this way. ",
        "style": "gentle and empathetic"
    },
    "anger": {
        "prefix": "I understand your frustration. ",
        "style": "calm and understanding"
    },
    "fear": {
        "prefix": "It's okay, you're safe here. ",
        "style": "reassuring and clear"
    },
    "disgust": {
        "prefix": "I hear you, that sounds really uncomfortable. ",
        "style": "validating and composed"
    },
    "surprise": {
        "prefix": "Oh wow, that's quite something! ",
        "style": "curious and engaged"
    },
    "neutral": {
        "prefix": "",
        "style": "helpful and balanced"
    }
}


class EIChatbot:
    """
    Emotionally Intelligent Chatbot.
    
    Architecture:
      1. Detect emotion in user message (EmotionDetector)
      2. Select appropriate response style (EMOTION_STYLE map)
      3. Prepend emotional acknowledgment prefix
      4. Generate response using DialoGPT
      5. Log everything for thesis analysis

    This is the KEY differentiator vs TraditionalChatbot.
    Same base model — different emotional intelligence layer.
    """

    MODEL_NAME = "microsoft/DialoGPT-medium"

    def __init__(self):
        print("🔄 Loading EI Chatbot model + Emotion Detector...")

        # Load DialoGPT — same base model as Traditional bot
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.MODEL_NAME,
            padding_side="left"
        )
        self.model = AutoModelForCausalLM.from_pretrained(self.MODEL_NAME)

        # Load emotion detector — this is what makes it "intelligent"
        self.emotion_detector = EmotionDetector()

        # Conversation state
        self.chat_history_ids = None
        self.turn_count = 0

        # Session log — stores every turn with emotion data
        # This feeds directly into your thesis analysis (OBJ 3)
        self.session_log = []

        print("✅ EI Chatbot ready!")

    def respond(self, user_input: str) -> dict:
        """
        Generate an emotionally aware response.

        Args:
            user_input: raw text from user

        Returns:
            {
                "response": str,
                "turn": int,
                "bot_type": "ei",
                "detected_emotion": str,
                "emotion_confidence": float,
                "emotion_scores": dict,
                "style_applied": str
            }
        """
        if not user_input or not user_input.strip():
            raise ValueError("User input cannot be empty")

        # ── STEP 1: Detect emotion ──────────────────────────────────
        emotion_data = self.emotion_detector.detect(user_input)
        dominant_emotion = emotion_data["dominant_emotion"]
        style = EMOTION_STYLE[dominant_emotion]

        # ── STEP 2: Build emotionally-aware input ───────────────────
        # We prepend an acknowledgment prefix to guide the response
        # Example: "I understand your frustration. why does nothing work?"
        augmented_input = style["prefix"] + user_input

        # ── STEP 3: Encode + append history ────────────────────────
        new_input_ids = self.tokenizer.encode(
            augmented_input + self.tokenizer.eos_token,
            return_tensors="pt"
        )

        if self.chat_history_ids is not None:
            input_ids = torch.cat(
                [self.chat_history_ids, new_input_ids], dim=-1
            )
        else:
            input_ids = new_input_ids

        # Limit context window
        if input_ids.shape[-1] > 1000:
            input_ids = input_ids[:, -1000:]

        # ── STEP 4: Generate response ───────────────────────────────
        self.chat_history_ids = self.model.generate(
            input_ids,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(
            self.chat_history_ids[:, input_ids.shape[-1]:][0],
            skip_special_tokens=True
        )

        self.turn_count += 1

        # ── STEP 5: Log for thesis analysis ────────────────────────
        log_entry = {
            "turn": self.turn_count,
            "user_input": user_input,
            "detected_emotion": dominant_emotion,
            "emotion_confidence": emotion_data["confidence"],
            "emotion_scores": emotion_data["all_scores"],
            "style_applied": style["style"],
            "prefix_used": style["prefix"],
            "bot_response": response,
        }
        self.session_log.append(log_entry)

        return {
            "response": response,
            "turn": self.turn_count,
            "bot_type": "ei",
            "detected_emotion": dominant_emotion,
            "emotion_confidence": emotion_data["confidence"],
            "emotion_scores": emotion_data["all_scores"],
            "style_applied": style["style"]
        }

    def get_session_summary(self) -> dict:
        """
        Returns full session analysis.
        Use this at end of conversation to collect thesis data.
        """
        if not self.session_log:
            return {"error": "No conversation data yet"}

        emotions_detected = [e["detected_emotion"] for e in self.session_log]
        emotion_counts = {e: emotions_detected.count(e) for e in set(emotions_detected)}

        return {
            "total_turns": self.turn_count,
            "emotions_detected": emotion_counts,
            "dominant_emotion_overall": max(emotion_counts, key=emotion_counts.get),
            "full_log": self.session_log
        }

    def reset(self):
        """Clear session — call between users in your research study."""
        self.chat_history_ids = None
        self.turn_count = 0
        self.session_log = []