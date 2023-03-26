from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Модель для получения информации о пользователях."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Модель для регистрации пользователя."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Модель для изменение профиля пользователя."""

    pass
