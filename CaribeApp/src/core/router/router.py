import flet as ft

from enum import Enum
from src.modules.pullovers.container.pullovers import Pullovers
from src.modules.about.container.about import About
from src.core.router.pages import Pages
from src.core.components.sidebar import Sidebar
from src.core.components.navbar import Navbar

routes = {
    Pages.PULLOVERS: Pullovers(),
    Pages.ABOUT: About(),
}


def on_route_change(page: ft.Page, e: ft.RouteChangeEvent):
    page.views.append(
        ft.View(
            "/",
            controls=[routes[Pages.PULLOVERS]],
        )
    )
    page.update()


def initial_view(page: ft.Page):
    page.views.append(
        ft.View(
            "/",
            controls=[routes[Pages.PULLOVERS]],
        )
    )
    page.on_route_change = lambda e: on_route_change(page, e)
    page.update()
