from fastapi import APIRouter
from .authors import router as author_router
from .qoutes import router as qouter_router

router = APIRouter(prefix="/v1")
router.include_router(author_router)
router.include_router(qouter_router)