import flet
from flet import (
    AppBar,
    Icon,
    IconButton,
    Page,
    PopupMenuButton,
    PopupMenuItem,
    Text,
    colors,
    icons,
    ThemeMode,
    cupertino_icons,
)
import flet as ft

from modules.core.components.navbar import Navbar
from modules.core.theme.colors import CARIBE_COLORS


def main(page: Page):
    page.theme_mode = ThemeMode.LIGHT

    page.appbar = Navbar(
        title="Caribe Demo",
        page=page,
    )

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dismissal(e):
        page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.selected_index}"))
        # page.close(drawer)

    drawer = ft.NavigationDrawer(
        on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )
    page.drawer = drawer

    def handle_click(e):
        page.drawer.open = not page.drawer.open
        page.update()

    page.add(
        ft.ElevatedButton(
            "Show drawer" if not page.drawer.open else "Hide Drawer",
            on_click=handle_click,
        )
    )

    page.add(Text("Body!"))


flet.app(target=main)
