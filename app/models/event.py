from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(String(1000))

    why_it_matters: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latest_development: Mapped[str | None] = mapped_column(
    Text,
    nullable=True,
    )

    what_happens_next: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    impact_scope: Mapped[str] = mapped_column(
        String(50),
        default="Unknown",
    )

    confidence: Mapped[str] = mapped_column(
        String(20),
        default="Developing",
    )

    editorial_priority: Mapped[str] = mapped_column(
        String(20),
        default="Background",
    )

    homepage: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    homepage_section: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    briefing_rank: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    importance_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    article_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    source_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        default="Other",
    )

    needs_refresh: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="Candidate",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    articles = relationship(
        "Article",
        back_populates="event",
    )