from typing import Optional, List, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


ModelType = TypeVar('ModelType')


class BaseCRUD:

    def __init__(self, model) -> None:
        self.model = model

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[int] = None,
        commit: bool = True
    ) -> ModelType:
        """Создание объекта и сохранение в БД."""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        if commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> ModelType:
        """Получение объекта из БД по id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ) -> List[ModelType]:
        """Получение всех обьектов из БД."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def get_investment_active(
        self,
        session: AsyncSession,
        obj
    ) -> ModelType:
        """Получение из БД первых по очереди незакрытых проектов и пожертвований."""
        db_obj = await session.execute(
            select(obj).where(
                obj.fully_invested == 0
            )
        )
        return db_obj.scalars().all()
