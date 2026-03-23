# backend/app/routes/analytics.py
# These endpoints power your OBJ 3 & 4 thesis analysis

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models import ChatSession, ChatMessage, User

router = APIRouter()


@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)):
    """Overall research summary — goes in your thesis results chapter."""

    total_sessions = await db.scalar(select(func.count(ChatSession.id)))
    total_messages = await db.scalar(select(func.count(ChatMessage.id)))

    # Average satisfaction per bot type
    ei_satisfaction = await db.scalar(
        select(func.avg(ChatSession.satisfaction))
        .where(ChatSession.bot_type == "ei")
    )
    trad_satisfaction = await db.scalar(
        select(func.avg(ChatSession.satisfaction))
        .where(ChatSession.bot_type == "traditional")
    )

    # Most common emotions detected
    emotion_counts = await db.execute(
        select(ChatMessage.detected_emotion, func.count(ChatMessage.id))
        .where(ChatMessage.detected_emotion.isnot(None))
        .group_by(ChatMessage.detected_emotion)
        .order_by(func.count(ChatMessage.id).desc())
    )

    return {
        "total_sessions":          total_sessions,
        "total_messages":          total_messages,
        "avg_satisfaction": {
            "ei_bot":          round(ei_satisfaction or 0, 2),
            "traditional_bot": round(trad_satisfaction or 0, 2),
        },
        "emotion_distribution": dict(emotion_counts.fetchall()),
    }


@router.get("/sessions")
async def get_all_sessions(db: AsyncSession = Depends(get_db)):
    """Returns all session data — export this for thesis analysis."""
    result = await db.execute(select(ChatSession))
    sessions = result.scalars().all()
    return [
        {
            "session_id":     s.session_id,
            "bot_type":       s.bot_type,
            "turn_count":     s.turn_count,
            "satisfaction":   s.satisfaction,
            "sentiment_shift": s.sentiment_shift,
            "started_at":     str(s.started_at),
        }
        for s in sessions
    ]