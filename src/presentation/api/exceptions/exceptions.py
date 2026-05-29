from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.core.application.exceptions.not_found_exception import NotFoundException
from src.core.application.exceptions.auth import UnauthorizedError

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedError) -> JSONResponse:
    return JSONResponse(
        status_code=403,
        content={"detail": str(exc)}
    )

async def not_found_exception_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(UnauthorizedError, unauthorized_exception_handler)
    app.add_exception_handler(NotFoundException, not_found_exception_handler)