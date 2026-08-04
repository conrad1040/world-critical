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
    latest_development: str | None = None
    why_it_matters: str | None
    what_happens_next: str | None
    impact_scope: str
    confidence: str
    homepage: bool
    category: str
    importance_score: int
    status: str
    article_count: int
    source_count: int
    created_at: datetime
    updated_at: datetime
    sources: list[str]
    articles: list[ArticleResponse]
    editorial_priority: str