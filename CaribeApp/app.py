import flet as ft
from src.core.router.router import initial_view
from src.core.theme.colors import THEME, DARK_THEME
from src.core.components.sidebar import Sidebar
from src.core.components.navbar import Navbar


def main(page: ft.Page):
    page.title = "CaribeApp"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = THEME
    page.dark_theme = DARK_THEME
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    initial_view(page)
    page.update()


ft.app(main)
