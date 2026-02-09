import flet as ft
from infrastructure.database import init_db, async_session
from infrastructure.repositories.product_repository import SQLProductRepository
from application.product_service import ProductService
from presentation.views.product_view import ProductView


async def main(page: ft.Page):
    page.title = "Punto de Venta - Clean Architecture"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    # 1. Inicializar Base de Datos (Crea tablas si no existen)
    await init_db()

    # 2. Inyección de Dependencias
    # Repository necesita la factory de sesiones
    repository = SQLProductRepository(async_session)
    service = ProductService(repository)
    product_view = ProductView(service)

    # 3. UI
    # View necesita el service
    product_view = ProductView(service)

    page.add(product_view)


if __name__ == "__main__":
    ft.run(main)
