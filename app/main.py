from fastapi import FastAPI
from app.routes import fund_routes, auth_routes
from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions import AppException

app = FastAPI()

app.include_router(fund_routes.router)
app.include_router(auth_routes.router)

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail
        }
    )