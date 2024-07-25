from typing import Any
import flet as ft
from modules.core.theme.colors import CARIBE_COLORS


class Navbar(ft.AppBar):
    def __init__(
        self,
        /,
        page: ft.Page,
        title: str = "Caribe Demo",
    ) -> None:

        super().__init__()
        self.page = page
        self.leading = ft.Icon(ft.icons.PALETTE)
        self.leading_width = 40
        self.title = ft.Text(title)
        self.center_title = False
        self.color = CARIBE_COLORS[self.page.theme_mode]["fontColorOnPrimary"]
        self.bgcolor = CARIBE_COLORS[self.page.theme_mode]["primary"]

        self.switchComponent = ft.Switch(
            thumb_icon=(
                ft.cupertino_icons.SUN_MAX
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else ft.cupertino_icons.MOON
            ),
            active_color=("#210339"),
            track_color=(
                ft.colors.ORANGE_600
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else "#210339"
            ),
            track_outline_color="transparent",
            inactive_thumb_color=(ft.colors.ORANGE_900),
            on_change=self.switch_theme,
        )

        self.openMenu = ft.IconButton(
            icon=ft.icons.MENU,
            on_click=self.open_menu(),
        )

        self.actions = [self.switchComponent]

    def open_menu(self) -> None:
        pass

    def switch_theme(self, _) -> None:
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.switchComponent.thumb_icon = (
            ft.cupertino_icons.SUN_MAX
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.cupertino_icons.MOON
        )

        self.switchComponent.track_color = (
            ft.colors.ORANGE_600
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else "#210339"
        )

        self.color = CARIBE_COLORS[self.page.theme_mode]["fontColorOnPrimary"]
        self.bgcolor = CARIBE_COLORS[self.page.theme_mode]["primary"]

        for key, value in CARIBE_COLORS[self.page.theme_mode].items():
            try:
                setattr(self.page, key, value)
            except AttributeError:
                pass

        self.page.update()
