from typing import List
from fastapi.routing import APIRouter
from fastapi.param_functions import Depends, Path, Security
from .models.domain.todos import TodoItem
from .models.schemas.todos import TodoCreateRequest, TodoUpdateRequest
from starlette import status
from ..auth.services import get_current_active_user
from ..auth.models.domain.users import User
from . import services
from .repository.fake import todos as todos_repository
from .exceptions import TodoNotFoundException


todos = APIRouter()

__valid_seqno = Path(..., ge=1)
__current_active_user = Depends(get_current_active_user)
__createable_user = Security(get_current_active_user, scopes=["TODO/POST"])
__readable_user = Security(get_current_active_user, scopes=["TODO/GET"])
__updateable_user = Security(get_current_active_user, scopes=["TODO/PATCH"])
__deleteable_user = Security(get_current_active_user, scopes=["TODO/DELETE"])


@todos.get(path="/{seqno}", response_model=TodoItem)
async def get_todo(
    seqno: int = __valid_seqno, current_user: User = __readable_user
) -> TodoItem:
    """ get todo item """
    todo = services.get_todo(db=todos_repository, seqno=seqno)
    if not todo:
        raise TodoNotFoundException
    return todo


@todos.get("", response_model=List[TodoItem])
async def get_todos(current_user: User = __readable_user) -> List[TodoItem]:
    """ get todos """
    todos = services.get_all(db=todos_repository)
    if not todos:
        raise TodoNotFoundException
    return todos


@todos.post("", status_code=status.HTTP_201_CREATED, response_model=TodoItem)
async def create_todo(
    todo: TodoCreateRequest, current_user: User = __createable_user
) -> TodoItem:
    """ create todo """
    return services.create_todo(db=todos_repository, todo=todo)


@todos.patch(
    path="/{seqno}", status_code=status.HTTP_200_OK, response_model=TodoItem
)
async def update_todo(
    todo_update_request: TodoUpdateRequest,
    seqno: int = __valid_seqno,
    current_user: User = __updateable_user,
) -> TodoItem:
    """ update todo """
    todo = services.get_todo(db=todos_repository, seqno=seqno)
    if not todo:
        raise TodoNotFoundException

    updated_todo = services.update_todo(
        db=todos_repository,
        seqno=seqno,
        previous_todo=todo,
        todo_update_request=todo_update_request,
    )

    return updated_todo


@todos.delete(path="/{seqno}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    seqno: int = __valid_seqno, current_user: User = __deleteable_user
) -> None:
    """ delete todo """
    todo = services.get_todo(db=todos_repository, seqno=seqno)
    if not todo:
        raise TodoNotFoundException
    services.delete_todo(db=todos_repository, seqno=seqno)
    return
