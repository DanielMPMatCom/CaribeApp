import flet as ft
from src.core.router.router import initial_view
from src.core.theme.colors import THEME, DARK_THEME
from src.core.components.sidebar import Sidebar
from src.core.components.navbar import Navbar


def main(page: ft.Page):
    page.title = "CaribeApp"
    page.scroll = ft.ScrollMode.HIDDEN

    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = THEME
    page.dark_theme = DARK_THEME
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = Navbar(page)
    page.drawer = Sidebar(page)
    initial_view(page)
    page.update()


ft.app(target=main)
