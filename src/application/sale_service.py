from datetime import datetime
from typing import List, Dict
from domain.models import Sale, SaleDetail
from domain.interfaces import ISaleRepository

class SaleService:
    def __init__(self, repository: ISaleRepository):
        self.repository = repository

    async def process_sale(self, cart_items: List[Dict]) -> Sale:
        """
        Recibe items del carrito: [{'product': Product, 'quantity': int, ...}]
        """
        if not cart_items:
            raise ValueError("El carrito está vacío")

        # 1. Calcular Totales
        total_sale = sum(item['subtotal'] for item in cart_items)

        # 2. Crear Objeto Venta (Encabezado)
        new_sale = Sale(
            total=total_sale,
            date=datetime.now(),
            client_id=None # Por ahora venta anónima
        )

        # 3. Crear Objetos Detalle
        details = []
        for item in cart_items:
            product = item['product']
            qty = item['quantity']
            
            detail = SaleDetail(
                sale_id=0, # Se asignará en el repositorio
                product_id=product.id,
                quantity=qty,
                unit_price=product.price,
                subtotal=item['subtotal']
            )
            details.append(detail)

        # 4. Llamar al repositorio
        return await self.repository.create_sale(new_sale, details)