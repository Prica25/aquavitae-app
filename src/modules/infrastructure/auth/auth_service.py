from typing import Optional

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.types.exceptions_type import UnauthorizedException
from src.core.utils.hash_utils import validate_hash
from src.modules.infrastructure.user import User
from src.modules.infrastructure.user.user_interface import UserInterface
from src.core.utils.image_utils import ImageUtils
from .dto.login_payload_dto import LoginPayloadDto
from .jwt_service import create_access_token


class AuthService:
    def __init__(self):
        self.user_interface = UserInterface()
        self.image_utils = ImageUtils("/src/static/images/profile_photo")

    # ---------------------- PUBLIC METHODS ----------------------
    async def login_user(
        self, user_login_dto: OAuth2PasswordRequestForm, db: Session
    ) -> Optional[LoginPayloadDto]:
        user = await self.__validate_user(db, user_login_dto)
        
        access_token = create_access_token(
            {
                "user_id": str(user.id),
                "user_email": user.email,
                "user_role": user.role.value,
            }
        )

        response = LoginPayloadDto(
            user=user,
            expires_in=access_token.expires_in,
            access_token=access_token.access_token,
            token_type=access_token.token_type,
        )

        await self.user_interface.update_last_access(db, str(user.id))

        response.user.profile_photo = self.image_utils.get_image(user.profile_photo)

        return response

    # ---------------------- PRIVATE METHODS ----------------------
    async def __validate_user(
        self, db: Session, user_login_dto: OAuth2PasswordRequestForm
    ) -> Optional[User]:
        user = await self.user_interface.find_one_user(
            db, {"where": User.email == user_login_dto.username}
        )

        if user and validate_hash(user_login_dto.password, user.password):
            return user

        raise UnauthorizedException(f"Invalid credentials.", ["User", "password"])
