from pydantic import BaseModel
from typing import Optional


class TodoCreateRequest(BaseModel):
    """ todo create request schema"""

    title: str
    content: Optional[str]
    is_done: bool = False


class TodoUpdateRequest(BaseModel):
    """ todo update request schema """

    title: str
    content: str
    is_done: bool
