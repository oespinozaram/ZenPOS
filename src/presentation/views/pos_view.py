import flet as ft
from application.product_service import ProductService
from application.sale_service import SaleService


class PosView(ft.Column):
    def __init__(self, product_service: ProductService, sale_service: SaleService):
        super().__init__(expand=True)
        self.product_service = product_service 
        self.sale_service = sale_service
        self.cart = [] 
        self.all_products = [] 
        
        # --- UI COMPONENTS ---
        
        # 1. Buscador
        self.search_input = ft.TextField(
            label="Escanear Código o Buscar Producto", 
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self.search_product,
            expand=True,
            autofocus=True
        )
        
        # 2. Tabla de Items (El Ticket)
        self.cart_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Producto")),
                ft.DataColumn(ft.Text("Cant"), numeric=True),
                ft.DataColumn(ft.Text("Precio"), numeric=True),
                ft.DataColumn(ft.Text("Total"), numeric=True),
                ft.DataColumn(ft.Text("")), 
            ],
            rows=[],
            expand=True,
            width=float("inf")
        )
        
        # 3. Totales y Botón de Pago
        self.total_text = ft.Text("$0.00", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
        self.pay_btn = ft.Button(
            "COBRAR", 
            icon=ft.Icons.PAYMENT,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN, 
                color=ft.Colors.WHITE,
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            width=200,
            height=60,
            on_click=self.process_payment
        )

        # --- LAYOUT PRINCIPAL ---
        self.controls = [
            ft.Row([
                # COLUMNA IZQUIERDA: Ticket / Tabla
                ft.Container(
                    content=ft.Column([
                        ft.Text("Ticket de Venta", size=20, weight="bold"),
                        ft.Container(
                            content=self.cart_table,
                            border=ft.border.Border.all(1, ft.Colors.OUTLINE),
                            border_radius=10,
                            expand=True,
                            padding=10
                        )
                    ]),
                    expand=2, 
                    padding=10
                ),
                
                # COLUMNA DERECHA: Buscador y Totales
                ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=self.search_input,
                            padding=10,
                            # --- CORRECCIÓN 1: Usamos un color seguro (Gris 200) ---
                            bgcolor=ft.Colors.GREY_200, 
                            border_radius=10
                        ),
                        ft.Divider(),
                        ft.Container(expand=True), 
                        ft.Column([
                            ft.Text("Total a Pagar:", size=16),
                            self.total_text,
                            ft.Container(height=20),
                            self.pay_btn
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ]),
                    expand=1, 
                    padding=10,
                    # --- CORRECCIÓN 2: Forma correcta de usar opacidad ---
                    # Usamos ft.colors.with_opacity(opacidad, color)
                    bgcolor=ft.Colors.with_opacity(0.3, ft.Colors.GREY_200),
                    border_radius=10
                )
            ], expand=True)
        ]

    def did_mount(self):
        self.page.run_task(self.load_initial_data)

    async def load_initial_data(self):
        self.all_products = await self.product_service.list_products()

    async def search_product(self, e):
        query = self.search_input.value.lower()
        if not query: return
        
        found = None
        for p in self.all_products:
            # Búsqueda segura convirtiendo a string por si acaso
            if str(p.barcode) == query or query in p.name.lower():
                found = p
                break
        
        if found:
            self.add_to_cart(found)
            self.search_input.value = ""
            self.search_input.focus()
            self.update()
        else:
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text("Producto no encontrado"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

    def add_to_cart(self, product):
        for item in self.cart:
            if item['product'].id == product.id:
                item['quantity'] += 1
                item['subtotal'] = item['quantity'] * item['product'].price
                self.refresh_table()
                return

        self.cart.append({
            "product": product,
            "quantity": 1,
            "subtotal": product.price
        })
        self.refresh_table()

    def remove_from_cart(self, product_id):
        self.cart = [item for item in self.cart if item['product'].id != product_id]
        self.refresh_table()

    def refresh_table(self):
        self.cart_table.rows.clear()
        total = 0.0
        
        for item in self.cart:
            p = item['product']
            qty = item['quantity']
            sub = item['subtotal']
            total += sub
            
            self.cart_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p.name)),
                    ft.DataCell(ft.Text(str(qty))),
                    ft.DataCell(ft.Text(f"${p.price:.2f}")),
                    ft.DataCell(ft.Text(f"${sub:.2f}", weight="bold")),
                    ft.DataCell(
                        ft.IconButton(
                            ft.Icons.DELETE, 
                            icon_color="red",
                            data=p.id, 
                            on_click=lambda e, pid=p.id: self.remove_from_cart(pid)
                        )
                    ),
                ])
            )
        
        self.total_text.value = f"${total:.2f}"
        self.update()

    async def process_payment(self, e):
        if not self.cart:
            return
            
        self.pay_btn.disabled = True
        self.update()

        try:
            # --- LLAMADA REAL A LA BASE DE DATOS ---
            await self.sale_service.process_sale(self.cart)

            # Éxito
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text("¡Venta Guardada y Stock Actualizado!"), bgcolor="green")
                self.page.snack_bar.open = True
                self.page.update()

            # Limpiar todo
            self.cart = []
            self.refresh_table()
            # Recargar productos para traer el stock actualizado
            await self.load_initial_data() 

        except ValueError as ve:
            # Error de validación (ej. Stock insuficiente)
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Error: {str(ve)}"), bgcolor="orange")
                self.page.snack_bar.open = True
                self.page.update()

        except Exception as ex:
            # Error técnico
            print(f"Error venta: {ex}")
            if self.page:
                self.page.snack_bar = ft.SnackBar(ft.Text("Error al procesar venta"), bgcolor="red")
                self.page.snack_bar.open = True
                self.page.update()

        finally:
            # Reactivar botón
            self.pay_btn.disabled = False
            self.update()