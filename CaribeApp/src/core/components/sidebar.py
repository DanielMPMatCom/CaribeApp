import flet as ft
from src.core.router.pages import Pages


class Sidebar(ft.NavigationDrawer):
    def __init__(self, /, page: ft.Page):
        def change_route(e):
            if e.control.selected_index == 0:
                page.go(Pages.PULLOVERS.value)
            elif e.control.selected_index == 1:
                page.go(Pages.ABOUT.value)
            # add your routes here...

        ft.NavigationDrawer.__init__(
            self,
            elevation=40,
            selected_index=0,
            on_change=change_route,
            controls=[
                ft.Container(height=12),
                ft.Container(
                    height=36,
                    alignment=ft.Alignment(0, 1),
                    content=ft.Text(
                        "Juegos Caribe",
                        size=22,
                        text_align="center",
                    ),
                ),
                ft.Divider(
                    trailing_indent=16,
                    leading_indent=16,
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.cupertino_icons.COMMAND),
                    label="Pullovers",
                ),
                ft.NavigationDrawerDestination(
                    icon_content=ft.Icon(ft.cupertino_icons.QUESTION_CIRCLE),
                    label="Manual de Usuario",
                ),
            ],
        )
