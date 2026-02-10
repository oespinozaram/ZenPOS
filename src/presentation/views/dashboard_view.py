import flet as ft
import flet_charts as fch

class DashboardView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=20)
        
        # Tarjetas de Métricas (KPIs)
        self.kpi_row = ft.Row(
            controls=[
                self._build_kpi_card("Ventas Hoy", "$1,250.00", ft.Icons.MONETIZATION_ON, "green"),
                self._build_kpi_card("Transacciones", "15", ft.Icons.RECEIPT_LONG, "blue"),
                self._build_kpi_card("Productos Bajos", "3", ft.Icons.WARNING_AMBER, "orange"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        # Gráfica de Ventas
        self.chart = fch.BarChart(
            groups=[
                fch.BarChartGroup(
                    x=0, 
                    rods=[fch.BarChartRod(from_y=0, to_y=40, width=20, color="blue", border_radius=5)]
                ),
                fch.BarChartGroup(
                    x=1, 
                    rods=[fch.BarChartRod(from_y=0, to_y=80, width=20, color="blue", border_radius=5)]
                ),
                fch.BarChartGroup(
                    x=2, 
                    rods=[fch.BarChartRod(from_y=0, to_y=30, width=20, color="blue", border_radius=5)]
                ),
                fch.BarChartGroup(
                    x=3, 
                    rods=[fch.BarChartRod(from_y=0, to_y=95, width=20, color="blue", border_radius=5)]
                ),
                fch.BarChartGroup(
                    x=4, 
                    rods=[fch.BarChartRod(from_y=0, to_y=60, width=20, color="blue", border_radius=5)]
                ),
            ],
            border=ft.border.Border.all(1, ft.Colors.GREY_400),
            left_axis=fch.ChartAxis(label_size=40, title=ft.Text("Ventas ($)")),
            bottom_axis=fch.ChartAxis(
                labels=[
                    fch.ChartAxisLabel(value=0, label=ft.Text("Lun")),
                    fch.ChartAxisLabel(value=1, label=ft.Text("Mar")),
                    fch.ChartAxisLabel(value=2, label=ft.Text("Mie")),
                    fch.ChartAxisLabel(value=3, label=ft.Text("Jue")),
                    fch.ChartAxisLabel(value=4, label=ft.Text("Vie")),
                ],
                label_size=30,
            ),
            horizontal_grid_lines=fch.ChartGridLines(
                color=ft.Colors.GREY_300, 
                width=1, 
                dash_pattern=[3, 3]
            ),
            # --- CORRECCIÓN FINAL ---
            # Configuración mínima y segura del tooltip
            tooltip=fch.BarChartTooltip(
                bgcolor=ft.Colors.with_opacity(0.8, ft.Colors.GREY_900),
            ),
            # ------------------------
            max_y=110,
            expand=True
        )

        self.controls = [
            ft.Text("Resumen General", size=30, weight=ft.FontWeight.BOLD),
            self.kpi_row,
            ft.Container(height=20),
            ft.Text("Ventas de la Semana", size=20, weight=ft.FontWeight.W_500),
            ft.Container(
                content=self.chart,
                height=300,
                border=ft.border.Border.all(1, ft.Colors.OUTLINE),
                border_radius=10,
                padding=20
            )
        ]

    def _build_kpi_card(self, title, value, icon, color):
        return ft.Container(
            content=ft.Row([
                ft.Icon(icon, size=40, color=ft.Colors.WHITE),
                ft.Column([
                    ft.Text(title, color=ft.Colors.WHITE_70),
                    ft.Text(value, size=20, weight="bold", color=ft.Colors.WHITE),
                ])
            ]),
            bgcolor=color,
            padding=20,
            border_radius=10,
            expand=True,
            margin=5
        )