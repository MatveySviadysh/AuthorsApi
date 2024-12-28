from fastapi import APIRouter
from .authors import router as author_router  # убедитесь, что импорт правильный

router = APIRouter(prefix="/v1")
router.include_router(author_router)  # подключаем роутер авторов