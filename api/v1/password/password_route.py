from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/forgot-password")
async def forgot_password(request: Request):
    pass


@router.post("/reset-password")
async def reset_password(request: Request):
    pass


@router.post("/change-password")
async def change_password(request: Request):
    pass
