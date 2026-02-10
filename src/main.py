import flet as ft
from infrastructure.database import init_db, async_session

from infrastructure.repositories.product_repository import SQLProductRepository
from infrastructure.repositories.sale_repository import SQLSaleRepository

from application.product_service import ProductService
from application.sale_service import SaleService

# --- IMPORTS DE VISTAS (Aquí faltaba PosView) ---
from presentation.views.product_view import ProductView
from presentation.views.dashboard_view import DashboardView
from presentation.views.pos_view import PosView
from presentation.layout import MainLayout

async def main(page: ft.Page):
    page.title = "ZenPOS"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Inicializar DB
    await init_db()

    # --- INYECCIÓN DE DEPENDENCIAS ---
    # Product
    product_repo = SQLProductRepository(async_session)
    product_service = ProductService(product_repo)

    # Sale
    sale_repo = SQLSaleRepository(async_session)
    sale_service = SaleService(sale_repo)

    view_pos = PosView(product_service, sale_service)
    
    # Instancias de las Vistas
    view_dashboard = DashboardView()
    view_inventory = ProductView(product_service)
    view_pos = PosView(product_service, sale_service)
    view_clients = ft.Text("Módulo de Clientes (En construcción)", size=30) 

    # --- NAVEGACIÓN ---
    def handle_nav_change(index):
        if index == 0:
            layout.set_content(view_dashboard)
        elif index == 1:
            layout.set_content(view_pos)
        elif index == 2:
            layout.set_content(view_inventory)
        elif index == 3:
            layout.set_content(view_clients)

    # Crear Layout Principal
    layout = MainLayout(page, handle_nav_change)
    
    # Cargar vista inicial (Dashboard)
    layout.set_content(view_dashboard)

    page.add(layout)

if __name__ == "__main__":
    ft.run(main)
