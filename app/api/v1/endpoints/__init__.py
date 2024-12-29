from fastapi import APIRouter
from .authors import router as author_router

router = APIRouter(prefix="/v1")
router.include_router(author_router)