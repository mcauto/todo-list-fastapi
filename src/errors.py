"""
에러
"""
from typing import Union

from fastapi import status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import validation_error_response_definition
from pydantic import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse


async def http_exception_handler(
    _: Request, exc: HTTPException
) -> JSONResponse:
    """ http exception handling """
    return JSONResponse({"errors": [exc.detail]}, status_code=exc.status_code)


async def validation_exception_handler(
    _: Request, exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """ client request exception handling """
    return JSONResponse(
        {"errors": exc.errors()}, status_code=status.HTTP_400_BAD_REQUEST
    )


validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": "{0}ValidationError".format(REF_PREFIX)},
    }
}
