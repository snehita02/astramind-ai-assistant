from pydantic import BaseModel
from typing import Any, List, Optional


class StandardResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class RAGResponse(BaseModel):
    question: str
    answer: str
    context_used: List[str]
    session_id: str
    tool_used: Optional[str] = None
    evaluation_enabled: bool