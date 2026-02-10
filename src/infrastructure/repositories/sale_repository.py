from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from domain.models import Sale, SaleDetail, Product
from domain.interfaces import ISaleRepository

class SQLSaleRepository(ISaleRepository):
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def create_sale(self, sale: Sale, details: List[SaleDetail]) -> Sale:
        async with self.session_factory() as session:
            try:
                # 1. Guardar el Encabezado de la Venta
                session.add(sale)
                await session.flush() # Genera el ID de la venta sin hacer commit aún
                await session.refresh(sale)

                # 2. Procesar cada item
                for detail in details:
                    # Asignar el ID de la venta recién creada
                    detail.sale_id = sale.id
                    session.add(detail)

                    # 3. Descontar Stock (Validación crítica)
                    product = await session.get(Product, detail.product_id)
                    if not product:
                        raise ValueError(f"Producto ID {detail.product_id} no existe")
                    
                    if product.stock < detail.quantity:
                        raise ValueError(f"Stock insuficiente para {product.name}")

                    product.stock -= detail.quantity
                    session.add(product) # Marcamos el producto para actualización

                # 4. Confirmar TODO junto
                await session.commit()
                await session.refresh(sale)
                return sale
                
            except Exception as e:
                await session.rollback() # Si algo falla, deshacemos todo
                raise e