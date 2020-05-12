"""
todos.py
"""
from typing import Optional, List, Dict

from fastapi.routing import APIRouter
from fastapi.param_functions import Path, Depends
from fastapi.exceptions import HTTPException
from fastapi import status
from pydantic import BaseModel
from .token import get_current_active_user, User

todos = APIRouter()


class TodoItem(BaseModel):
    """ todo schema """

    seqno: int
    title: str
    content: Optional[str]
    is_done: bool


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


__fake_todos: Dict[int, TodoItem] = {}


def __get_last_seqno() -> int:
    sorted_todos = sorted(__fake_todos.items())
    last_seqno = sorted_todos[-1][0] if sorted_todos else 0
    return last_seqno


__valid_seqno = Path(..., ge=1)
__current_active_user = Depends(get_current_active_user)


@todos.get(path="/{seqno}", response_model=TodoItem)
async def get_todo(
    seqno: int = __valid_seqno, current_user: User = __current_active_user
) -> TodoItem:
    """ get todo item """
    return __get_todo(seqno=seqno)


def __get_todo(seqno: int) -> TodoItem:
    todo = __fake_todos.get(seqno, None)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return todo


@todos.get("", response_model=List[TodoItem])
async def get_todos(
    current_user: User = __current_active_user
) -> List[TodoItem]:
    """ get todos """
    return __get_all()


def __get_all() -> List[TodoItem]:
    todos = [TodoItem(**todo.dict()) for todo in __fake_todos.values()]
    if not todos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="not found todolist"
        )
    return todos


@todos.post("", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def create_todo(
    todo: TodoCreateRequest, current_user: User = __current_active_user
) -> TodoItem:
    """ create todo """
    return __create_todo(todo)


def __create_todo(todo: TodoCreateRequest) -> TodoItem:
    next_seqno = __get_last_seqno() + 1
    new_todo = TodoItem(seqno=next_seqno, **todo.dict())
    __fake_todos[next_seqno] = new_todo
    return new_todo


@todos.patch(
    path="/{seqno}", status_code=status.HTTP_200_OK, response_model=TodoItem
)
async def update_todo(
    todo_update_request: TodoUpdateRequest,
    seqno: int = __valid_seqno,
    current_user: User = __current_active_user,
) -> TodoItem:
    """ update todo """
    todo = __get_todo(seqno=seqno)
    updated_todo = __update_todo(
        previous_todo=todo, todo_update_request=todo_update_request
    )
    __fake_todos[seqno] = updated_todo
    return updated_todo


def __update_todo(
    previous_todo: TodoItem, todo_update_request: TodoUpdateRequest
) -> TodoItem:
    """ TODO:  """
    if previous_todo.title != todo_update_request.title:
        previous_todo.title = todo_update_request.title
    if previous_todo.content != todo_update_request.content:
        previous_todo.content = todo_update_request.content
    if previous_todo.is_done != todo_update_request.is_done:
        previous_todo.is_done = todo_update_request.is_done
    return previous_todo


@todos.delete(path="/{seqno}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    seqno: int = __valid_seqno, current_user: User = __current_active_user
) -> None:
    """ delete todo """
    todo = __get_todo(seqno)
    __fake_todos.pop(todo.seqno)
    return
