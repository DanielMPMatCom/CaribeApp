import flet as ft
from src.core.theme.colors import THEME, DARK_THEME
from src.core.components.navbar import Navbar
from src.responsive_menu_layout import ResponsiveMenuLayout
from src.core.router.pages import pages
from src.core.components.sidebar import Sidebar


def main(page: ft.Page):
    page.title = "CaribeApp"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = THEME
    page.dark_theme = DARK_THEME
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    # layout = ResponsiveMenuLayout(page, pages=pages)
    page.drawer = Sidebar(
        page=page,
        selected=0,
    )

    def open_side_bar():
        page.drawer.open = not page.drawer.open

    page.appbar = Navbar(page, open_side_bar=open_side_bar)
    page.update()


ft.app(main)
