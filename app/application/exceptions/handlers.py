from fastapi import HTTPException, status
from starlette.requests import Request
from starlette.responses import JSONResponse


def user_not_found_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "message": "User not found"
        }
    )
