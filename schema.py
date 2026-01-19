from pydantic import BaseModel
from uuid import UUID

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: UUID
    title: str
    content: str