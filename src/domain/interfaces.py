from typing import Protocol, List, Optional
from .models import Product


class IProductRepository(Protocol):
    """Contrato que debe cumplir cualquier base de datos que usemos"""

    async def get_all(self) -> List[Product]:
        ...

    async def get_by_id(self, id: int) -> Optional[Product]:
        ...

    async def create(self, product: Product) -> Product:
        ...

