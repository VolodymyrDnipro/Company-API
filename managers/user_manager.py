from typing import TypeVar, Generic, List, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

ModelType = TypeVar("ModelType")


class CRUDBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[ModelType]:
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_id(self, model_id: int) -> ModelType:
        query = await self.session.execute(select(self.model).filter(self.model.user_id == model_id))
        return query.scalar_one()

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
