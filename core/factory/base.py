from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers import AuthController, UserController
from app.repositories import (
    UserProviderRepository,
    UserRepository,
    UserRoleRepository,
    VendorRepository,
)
from core.database import get_db


class Factory:
    # ============= Repository Layer =============
    @staticmethod
    def get_user_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> UserRepository:
        return UserRepository(session)

    @staticmethod
    def get_user_role_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> UserRoleRepository:
        return UserRoleRepository(session)

    @staticmethod
    def get_user_provider_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> UserProviderRepository:
        return UserProviderRepository(session)

    @staticmethod
    def get_vendor_repository(
        session: Annotated[AsyncSession, Depends(get_db)],
    ) -> VendorRepository:
        return VendorRepository(session)

    # ============= Controller Layer =============
    @staticmethod
    def get_auth_controller(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
        user_role_repository: Annotated[UserRoleRepository, Depends(get_user_role_repository)],
        user_provider_repository: Annotated[
            UserProviderRepository, Depends(get_user_provider_repository)
        ],
    ) -> AuthController:
        return AuthController(
            user_repository=user_repository,
            user_role_repository=user_role_repository,
            user_provider_repository=user_provider_repository,
        )

    @staticmethod
    def get_user_controller(
        user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    ) -> UserController:
        return UserController(user_repository)
