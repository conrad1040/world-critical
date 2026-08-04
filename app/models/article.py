from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(500),
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    url: Mapped[str] = mapped_column(
        String(1000),
        unique=True,
    )

    published_at: Mapped[datetime] = mapped_column(
        DateTime,
    )

    source_id: Mapped[int] = mapped_column(
        ForeignKey("sources.id"),
    )

    event_id: Mapped[int | None] = mapped_column(
        ForeignKey("events.id"),
        nullable=True,
    )

    processed_for_event: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    editorial_status: Mapped[str] = mapped_column(
    String(20),
    default="Pending",
    )

    source = relationship(
        "Source",
        back_populates="articles",
    )

    event = relationship(
        "Event",
        back_populates="articles",
    )