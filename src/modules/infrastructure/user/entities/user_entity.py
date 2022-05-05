from sqlalchemy import Column, Enum, event, String

from src.core.common.base_entity import BaseEntity
from src.core.constants.enum.user_role import UserRole
from src.core.utils.hash_utils import generate_hash, validate_hash


class User(BaseEntity):
    __tablename__ = 'user'

    name: str = Column(String(50), nullable=False)
    email: str = Column(String(120), unique=True, nullable=False)
    password: str = Column(String(120), nullable=False)
    role: UserRole = Column(Enum(UserRole), nullable=False, default=UserRole.USER)

    def __init__(self, name: str, email: str, password: str, role: UserRole = None, *args, **kwargs):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def check_password(self, password: str) -> bool:
        return validate_hash(self.password, password)


@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def before_insert(mapper, connection, target: User) -> None:
    if target.password:
        target.password = generate_hash(target.password)
