from fastapi import APIRouter
from router import i_mongo_op

router=APIRouter()
router.include_router(i_mongo_op.router)
