from typing import Any, List, Optional
from .models.domain.todos import TodoItem
from .models.schemas.todos import TodoCreateRequest, TodoUpdateRequest


def get_todo(db: Any, seqno: int) -> Optional[TodoItem]:
    todo: Optional[TodoItem] = db.get(seqno, None)
    return todo


def get_all(db: Any) -> List[TodoItem]:
    todos = [TodoItem(**todo.dict()) for todo in db.values()]
    return todos


def create_todo(db: Any, todo: TodoCreateRequest) -> TodoItem:
    next_seqno = get_last_seqno(db) + 1
    new_todo = TodoItem(seqno=next_seqno, **todo.dict())
    db[next_seqno] = new_todo
    return new_todo


def get_last_seqno(db: Any) -> int:
    sorted_todos = sorted(db.items())
    last_seqno: int = sorted_todos[-1][0] if sorted_todos else 0
    return last_seqno


def update_todo(
    db: Any,
    seqno: int,
    previous_todo: TodoItem,
    todo_update_request: TodoUpdateRequest,
) -> TodoItem:
    """ TODO:  """
    if previous_todo.title != todo_update_request.title:
        previous_todo.title = todo_update_request.title
    if previous_todo.content != todo_update_request.content:
        previous_todo.content = todo_update_request.content
    if previous_todo.is_done != todo_update_request.is_done:
        previous_todo.is_done = todo_update_request.is_done
    db[seqno] = previous_todo
    return previous_todo


def delete_todo(db: Any, seqno: int) -> None:
    db.pop(seqno)
    print(db)
