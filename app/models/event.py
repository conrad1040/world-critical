from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, DateTime, Integer, String

from app.database.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(1000))

    importance_score: Mapped[int] = mapped_column(Integer, default=0)

    article_count: Mapped[int] = mapped_column(Integer, default=0)
    source_count: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped[str] = mapped_column(
    String(50),
    default="Unknown",
    )

    category: Mapped[str] = mapped_column(
    String(50),
    default="Other",
    )

    needs_refresh: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    status: Mapped[str] = mapped_column(String(50), default="Candidate")

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    articles = relationship(
        "Article",
        back_populates="event",
    )