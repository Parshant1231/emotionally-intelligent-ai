# backend/app/routes/chat.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import ChatSession, User
from app.services.bot_service import bot_service
import uuid

router = APIRouter()


# ── Request/Response Schemas ─────────────────────────────────────
# Pydantic models validate incoming JSON automatically

class StartSessionRequest(BaseModel):
    bot_type:    str   = Field(..., pattern="^(ei|traditional)$")
    age_group:   str   = Field(default="unspecified")
    gender:      str   = Field(default="unspecified")
    tech_comfort: str  = Field(default="medium")

class StartSessionResponse(BaseModel):
    session_id: str
    bot_type:   str
    message:    str

class ChatRequest(BaseModel):
    session_id: str
    message:    str = Field(..., min_length=1, max_length=1000)
    bot_type:   str = Field(..., pattern="^(ei|traditional)$")

class ChatResponse(BaseModel):
    response:           str
    turn:               int
    bot_type:           str
    detected_emotion:   str | None = None
    emotion_confidence: float | None = None
    style_applied:      str | None = None

class EndSessionRequest(BaseModel):
    session_id:   str
    bot_type:     str
    satisfaction: float = Field(..., ge=1.0, le=5.0)  # 1-5 rating


# ── Routes ────────────────────────────────────────────────────────

@router.post("/start", response_model=StartSessionResponse)
async def start_session(req: StartSessionRequest, db: AsyncSession = Depends(get_db)):
    """
    Start a new chat session.
    Creates session record + user profile in DB.
    Frontend calls this before first message.
    """
    session_id = str(uuid.uuid4())

    # Save user characteristics (OBJ 2 data)
    user = User(
        session_id   = session_id,
        age_group    = req.age_group,
        gender       = req.gender,
        tech_comfort = req.tech_comfort,
    )
    db.add(user)

    # Create chat session record
    session = ChatSession(
        session_id      = session_id,
        user_session_id = session_id,
        bot_type        = req.bot_type,
    )
    db.add(session)
    await db.commit()

    return StartSessionResponse(
        session_id = session_id,
        bot_type   = req.bot_type,
        message    = "Session started. You can now send messages."
    )


@router.post("/message", response_model=ChatResponse)
async def send_message(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Send a message and get a bot response.
    Core endpoint — called on every chat turn.
    """
    try:
        result = await bot_service.chat(
            session_id = req.session_id,
            user_input = req.message,
            bot_type   = req.bot_type,
            db         = db
        )
        return ChatResponse(**result)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bot error: {str(e)}")


@router.post("/end")
async def end_session(req: EndSessionRequest, db: AsyncSession = Depends(get_db)):
    """
    End session + save satisfaction rating.
    Called when user submits post-chat survey.
    """
    try:
        result = await bot_service.end_session(
            session_id   = req.session_id,
            bot_type     = req.bot_type,
            satisfaction = req.satisfaction,
            db           = db
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))