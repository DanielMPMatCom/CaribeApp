from flet import (
    Page,
    colors,
    IconButton,
    icons,
    ElevatedButton,
    Text,
    Switch,
    Row,
    AppBar,
)
import flet


def main(page: Page, title="Basic Responsive Menu"):

    page.title = title

    menu_button = IconButton(icons.MENU)

    page.appbar = AppBar(
        leading=menu_button,
        leading_width=40,
        bgcolor=colors.SURFACE_VARIANT,
    )

    menu_layout = ResponsiveMenuLayout(page, pages)

    page.appbar.actions = [
        Row(
            [
                Text("Minimize\nto icons"),
                Switch(on_change=lambda e: toggle_icons_only(menu_layout)),
                Text("Menu\nwidth"),
                Switch(value=True, on_change=lambda e: toggle_menu_width(menu_layout)),
            ]
        )
    ]

    menu_layout.navigation_rail.leading = ElevatedButton(
        "Add", icon=icons.ADD, expand=True, on_click=lambda e: print("Add clicked")
    )

    page.add(menu_layout)

    menu_button.on_click = lambda e: menu_layout.toggle_navigation()


flet.app(target=main)
