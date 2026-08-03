from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(150), unique=True)
    website: Mapped[str] = mapped_column(String(500), unique=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)

    articles = relationship("Article", back_populates="source")