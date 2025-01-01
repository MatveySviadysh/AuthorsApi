from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.logger import app_logger, error_logger, access_logger
from api.v1.endpoints import router as api_router
import uvicorn

# Инициализация приложения FastAPI
app = FastAPI(
    title="Authors API",
    description="API для работы с авторами и их цитатами",
    version="1.0.0"
)

origins = [
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    app_logger.info("Приложение запущено")

@app.on_event("shutdown")
async def shutdown_event():
    app_logger.info("Приложение остановлено")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
