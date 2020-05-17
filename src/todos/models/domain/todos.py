from typing import Optional
from pydantic import BaseModel


class TodoItem(BaseModel):
    """ todo schema """

    seqno: int
    title: str
    content: Optional[str]
    is_done: bool
