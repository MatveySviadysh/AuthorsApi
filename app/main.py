from fastapi import FastAPI
from core.logger import app_logger, error_logger, access_logger
from api.v1.endpoints import router as api_router

app = FastAPI(
    title="Authors API",
    description="API для работы с авторами и их цитатами",
    version="1.0.0"
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    app_logger.info("Приложение запущено")

if __name__ == "__main__":
    pass
    