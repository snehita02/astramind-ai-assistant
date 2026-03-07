# from pydantic import BaseModel
# from typing import List, Optional, Dict


# class StandardResponse(BaseModel):

#     success: bool
#     message: str
#     data: Optional[dict]


# class RAGResponse(BaseModel):

#     question: str
#     answer: str

#     confidence: float

#     grounded: bool
#     grounding_score: float

#     sources: List[str]

#     top_contexts: List[Dict]

#     evaluation: Optional[str] = None

#     context_used: List[str]

#     session_id: str
#     tool_used: Optional[str]

#     evaluation_enabled: bool


from pydantic import BaseModel
from typing import List, Optional


class StandardResponse(BaseModel):

    success: bool
    message: str
    data: Optional[dict]


class RAGResponse(BaseModel):

    question: str
    answer: str

    confidence: float
    grounded: bool

    sources: List[str]

    evaluation: Optional[str]

    context_used: List[str]

    session_id: str
    tool_used: Optional[str]

    evaluation_enabled: bool