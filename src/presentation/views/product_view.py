import flet as ft
from application.product_service import ProductService


class ProductView(ft.Column):
    def __init__(self, service: ProductService):
        # En v0.80+, init debe ser ligero.
        super().__init__(expand=True, spacing=20)  # Pasamos props al super (Dataclass style)
        self.service = service

        # Componentes UI (Estado)
        self.name_input = ft.TextField(label="Nombre", expand=2)
        self.price_input = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER, expand=1)
        self.barcode_input = ft.TextField(label="Código Barras", expand=1)

        # Lista reactiva
        self.products_list = ft.ListView(expand=True, spacing=10, padding=20)

        # Construcción Declarativa del Layout
        self.controls = [
            ft.Container(
                content=ft.Text("Punto de Venta (v0.80.5)", size=28, weight=ft.FontWeight.BOLD),
                padding=10
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        self.name_input,
                        self.price_input,
                        self.barcode_input,
                        ft.Button(
                            "Agregar",
                            icon=ft.Icons.ADD,
                            on_click=self.add_product_click,  # Event Handler
                            style=ft.ButtonStyle(bgcolor=ft.Colors.PRIMARY, color=ft.Colors.WHITE)
                        )
                    ],
                    spacing=10
                ),
                padding=10,
                border=ft.border.Border.all(1, ft.Colors.OUTLINE),
                border_radius=10
            ),
            ft.Divider(),
            self.products_list
        ]

    def did_mount(self):
        """Ciclo de vida: Se ejecuta cuando el control se monta en la página."""
        self.page.run_task(self.load_products)

    async def load_products(self):
        # Verificamos que el control siga montado en la página
        if not self.page:
            return

        try:
            products = await self.service.list_products()

            self.products_list.controls.clear()
            for p in products:
                self.products_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(p.name),
                        subtitle=ft.Text(f"${p.price} | Stock: {p.stock}"),
                        leading=ft.Icon(ft.Icons.SHOPPING_BAG),
                        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.BLACK)  # Un poco de estilo
                    )
                )
            self.update()

        except Exception as e:
            print(f"Error cargando productos: {e}")

    async def add_product_click(self, e):
        """
        Manejador de Evento v0.80.5:
        Nota que NO llamamos a self.update() al final.
        Flet v0.80 lo hace automático al terminar la función async.
        """
        try:
            if not self.price_input.value:
                return  # Validación simple

            await self.service.add_new_product(
                name=self.name_input.value,
                price=float(self.price_input.value),
                stock=10,
                barcode=self.barcode_input.value
            )

            # Limpiar inputs
            self.name_input.value = ""
            self.price_input.value = ""
            self.barcode_input.value = ""

            # Recargar lista
            await self.load_products()

            # Feedback visual (SnackBar)
            # En v0.80 accedemos a page de forma segura
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text("Producto agregado!"))
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            print(f"Error detallado: {ex}")  # Imprime en consola para ver detalles
            if self.page:
                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Error: {str(ex)}"),
                    bgcolor="red"
                )
                self.page.snack_bar.open = True
                self.page.update()