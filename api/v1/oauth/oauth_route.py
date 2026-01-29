from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/{provider}")
async def social_provider(request: Request):
    pass


@router.get("/{provider}/callback")
async def social_provider_callback(request: Request):
    pass
