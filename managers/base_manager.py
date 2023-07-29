from typing import TypeVar, Generic, List, Type, Optional, Any
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import cast, String

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, **kwargs: Optional[Any]) -> List[ModelType]:
        stmt = select(self.model)
        if kwargs:
            stmt = stmt.filter_by(**kwargs)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_field(self, model_value, field_name: str) -> ModelType:
        print(self.model)
        filter_field = getattr(self.model, field_name)
        stmt = select(self.model).filter(cast(filter_field, String) == str(model_value))
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def get_by_fields(self, **kwargs: Any) -> Optional[ModelType]:
        stmt = select(self.model)
        for field_name, value in kwargs.items():
            filter_field = getattr(self.model, field_name)
            stmt = stmt.filter(cast(filter_field, String) == str(value))
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def create(self, obj: ModelType) -> ModelType:
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def update(self, obj: ModelType, update_data: dict) -> ModelType:
        for key, value in update_data.items():
            setattr(obj, key, value)
        merged_obj = await self.session.merge(obj)
        await self.session.commit()
        return merged_obj

    async def delete(self, obj: ModelType):
        await self.session.delete(obj)
        await self.session.commit()
