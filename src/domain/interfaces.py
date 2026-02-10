from typing import Protocol, List, Optional
from .models import Product, Sale, SaleDetail


class IProductRepository(Protocol):
    async def get_all(self) -> List[Product]: ...
    async def get_by_id(self, id: int) -> Optional[Product]: ...
    async def create(self, product: Product) -> Product: ...

class ISaleRepository(Protocol):
    async def create_sale(self, sale: Sale, details: List[SaleDetail]) -> Sale:
        """Guarda venta, detalles y actualiza stock en una transacción"""
        ...

