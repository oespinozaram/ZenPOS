import flet as ft

class MainLayout(ft.Row):
    def __init__(self, page: ft.Page, navigation_change_handler):
        super().__init__(expand=True)
        self.app_page = page 
        self.navigation_change_handler = navigation_change_handler

        # Menú Lateral
        self.rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=400,
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD_OUTLINED, 
                    selected_icon=ft.Icons.DASHBOARD, 
                    label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.POINT_OF_SALE, 
                    # --- CORRECCIÓN AQUÍ ---
                    # Eliminamos selected_icon_content. 
                    # Usamos selected_icon estándar.
                    selected_icon=ft.Icons.POINT_OF_SALE, 
                    # -----------------------
                    label="Punto de Venta"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY_2_OUTLINED, 
                    selected_icon=ft.Icons.INVENTORY_2, 
                    label="Inventario"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PEOPLE_OUTLINED, 
                    selected_icon=ft.Icons.PEOPLE, 
                    label="Clientes"
                ),
            ],
            on_change=self.on_nav_change,
        )

        self.content_area = ft.Container(expand=True, padding=20)

        self.controls = [
            self.rail,
            ft.VerticalDivider(width=1),
            self.content_area,
        ]

    def on_nav_change(self, e):
        self.navigation_change_handler(e.control.selected_index)

    def set_content(self, view_control):
        self.content_area.content = view_control
        try:
            # Intentamos actualizar el área de contenido
            self.content_area.update()
        except Exception:
            # Si el control no está en la página todavía (ej. al inicio del main),
            # update() fallaría o acceder a .page fallaría. 
            # No pasa nada, page.add() lo pintará después.
            pass