from fastapi import APIRouter

router = APIRouter()


@router.post("/api/v0/token/refresh")
async def token_refresh():
    pass


@router.post("/api/v0/token/invalidate")
async def token_invalidate():
    pass


@router.post("/api/v0/token/check")
async def token_check():
    pass
