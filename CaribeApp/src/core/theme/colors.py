from typing import Any
from flet import ThemeMode
import flet as ft


THEME: ft.Theme = ft.Theme(
    font_family="Roboto",
    use_material3=True,
    appbar_theme=ft.AppBarTheme(
        color="#8A0F12",
        foreground_color="#8A0F12",
        bgcolor="#FFFFFF",
        shadow_color="#000000",
        surface_tint_color="#FFFFFF",
        elevation=4,
        title_text_style=ft.TextStyle(
            size=22,
            color="#8A0F12",
            font_family="Roboto",
        ),
    ),
    navigation_drawer_theme=ft.NavigationDrawerTheme(
        bgcolor="#FFFFFF",
        shadow_color="#8A0F12",
        surface_tint_color="#FFFFFF",
        indicator_color="#8A0F12",
        elevation=4,
        tile_height=48,
        indicator_shape=ft.RoundedRectangleBorder(
            radius=8,
        ),
    ),
    primary_color="#8A0F12",
)


DARK_THEME: ft.Theme = ft.Theme(
    font_family="Roboto",
    appbar_theme=ft.AppBarTheme(
        color="#540002",
        foreground_color="#FFE3C8",
        bgcolor="#8A0F12",
        shadow_color="#FFE3C8",
        surface_tint_color="#8A0F12",
        elevation=4,
        title_text_style=ft.TextStyle(
            size=22,
            color="#FFE3C8",
            font_family="Roboto",
        ),
    ),
)
