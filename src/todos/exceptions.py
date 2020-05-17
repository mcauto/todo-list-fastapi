from fastapi.exceptions import HTTPException
from starlette import status

TodoNotFoundException = HTTPException(status_code=status.HTTP_404_NOT_FOUND)
