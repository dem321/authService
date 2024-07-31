from fastapi import APIRouter

router = APIRouter()


@router.post("/api/v0/login")
async def login():
    pass


@router.post("/api/v0/logout")
async def logout():
    pass


@router.post("/api/v0/register")
async def register():
    pass
