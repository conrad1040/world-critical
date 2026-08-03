from datetime import datetime

from pydantic import BaseModel


class ArticleResponse(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime


class EventResponse(BaseModel):
    id: int
    title: str
    summary: str
    category: str
    importance_score: int
    status: str
    article_count: int
    source_count: int
    created_at: datetime
    updated_at: datetime
    sources: list[str]
    articles: list[ArticleResponse]