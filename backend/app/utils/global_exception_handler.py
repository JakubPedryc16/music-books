from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.schemas.api_response import APIResponse
from app.utils.logger import logger
 
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            success=False,
            error=str(exc)
        ).model_dump()
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "message" in exc.detail:
        error_message = exc.detail["message"]
        error_code = exc.detail.get("code")
    else:
        error_message = exc.detail
        error_code = exc.status_code

    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            success=False,
            error=error_message,
            error_code=error_code
        ).model_dump()
    )

async def unhandled_exception_handler(request: Request, exc: Exception):
    error_detail = f"An unexpected server error occurred: {str(exc)}"
    logger.exception(error_detail)
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            success=False,
            error=error_detail,
            error_code="UNHANDLED_ERROR"
        ).model_dump()
    )
