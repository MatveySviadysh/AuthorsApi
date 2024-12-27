from api.v1.endpoints import authors
from db.queries.seeds import create_tables, insert_data
from fastapi import FastAPI
from core.config import settings
import asyncio
from core.logger import app_logger, error_logger, access_logger

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     version=settings.VERSION,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json"
# )

# app.include_router(authors.router, prefix=f"{settings.API_V1_STR}/authors", tags=["authors"])

# @app.get("/")
# def root():
#     return {"message": "Welcome to FastAPI application"}


if __name__ == "__main__":
    create_tables()
    insert_data()
    
    app_logger.info("Приложение запущено")
    error_logger.error("Произошла ошибка")
    access_logger.info("Получен запрос GET /authors")
    