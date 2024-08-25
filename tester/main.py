import flet as ft
from src.PuLP_Fictiton import PuLP_Solver
import pulp


def main(page: ft.Page):
    page.title = "CaribeApp"
    page.scroll = ft.ScrollMode.HIDDEN
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def A():
        # gurobipy
        try:
            assignation = PuLP_Solver(
                ["ISRI", "MATCOM", "DER", "TUR"],
                {"ISRI": 80, "MATCOM": 80, "DER": 20, "TUR": 50},
                {"ISRI": 1, "MATCOM": 2, "DER": 3, "TUR": 5},
                {"A": 100, "B": 100, "C": 100},
                50,
                30,
                {"ISRI": "A", "MATCOM": "B", "DER": "B", "TUR": "C"},
                solver_name="GUROBI",
            )

            for faculty, (pullovers, color) in assignation.items():
                print(f"{faculty}: {pullovers} pullovers colour {color}")

            print(pulp.listSolvers(onlyAvailable=True))
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Pincho"),
                action="Cerrar",
            )
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(
                content=ft.Text(e),
                action="Cerrar",
            )
            page.snack_bar.open = True
            page.update()

    page.add(ft.ElevatedButton("PLAY", on_click=lambda _: A()))
    page.update()


ft.app(target=main)
