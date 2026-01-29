from typing import Annotated

from fastapi import APIRouter, Query, Request
from pydantic import EmailStr

router = APIRouter()


@router.get("/verify")
async def verify_email(
    request: Request, email: Annotated[EmailStr, Query()], token: Annotated[str, Query()]
):
    return {"email": email, "token": token}


@router.post("/resend-verification")
async def resend_verification(request: Request):
    pass
