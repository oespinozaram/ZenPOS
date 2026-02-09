from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from domain.models import Product
from domain.interfaces import IProductRepository


class SQLProductRepository(IProductRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def get_all(self) -> List[Product]:
        async with self.session_factory() as session:
            statement = select(Product)
            result = await session.exec(statement)
            # .all() devuelve una lista de objetos.
            # Al salir del 'async with', la sesión se cierra.
            # SQLModel suele ser bueno con esto, pero para asegurar, devolvemos la lista directa.
            return result.all()

    async def create(self, product: Product) -> Product:
        async with self.session_factory() as session:
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product

    async def get_by_id(self, id: int) -> Optional[Product]:
        async with self.session_factory() as session:
            return await session.get(Product, id)
