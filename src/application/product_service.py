from domain.models import Product
from domain.interfaces import IProductRepository


class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    async def list_products(self):
        return await self.repository.get_all()

    async def add_new_product(self, name: str, price: float, stock: int, barcode: str):
        # Aquí podrías poner lógica de negocio (ej: validar código de barras)
        if price < 0:
            raise ValueError("El precio no puede ser negativo")

        new_product = Product(name=name, price=price, stock=stock, barcode=barcode)
        return await self.repository.create(new_product)