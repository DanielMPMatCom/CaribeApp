from flet import Row, Column, Card, Text, icons, Container


def create_page(title: str, body: str):
    return Row(
        controls=[
            Column(
                horizontal_alignment="stretch",
                controls=[
                    Card(content=Container(Text(title, weight="bold"), padding=8)),
                    Text(body),
                ],
                expand=True,
            ),
        ],
        expand=True,
    )


pages = [
    (
        dict(
            icon=icons.LANDSCAPE_OUTLINED,
            selected_icon=icons.LANDSCAPE,
            label="Menu in landscape",
        ),
        create_page(
            "Menu in landscape",
            "Menu in landscape is by default shown, side by side with the main content, but can be "
            "hidden with the menu button.",
        ),
    ),
    (
        dict(
            icon=icons.PORTRAIT_OUTLINED,
            selected_icon=icons.PORTRAIT,
            label="Menu in portrait",
        ),
        create_page(
            "Menu in portrait",
            "Menu in portrait is mainly expected to be used on a smaller mobile device."
            "\n\n"
            "The menu is by default hidden, and when shown with the menu button it is placed on top of the main "
            "content."
            "\n\n"
            "In addition to the menu button, menu can be dismissed by a tap/click on the main content area.",
        ),
    ),
    (
        dict(
            icon=icons.INSERT_EMOTICON_OUTLINED,
            selected_icon=icons.INSERT_EMOTICON,
            label="Minimize to icons",
        ),
        create_page(
            "Minimize to icons",
            "ResponsiveMenuLayout has a parameter minimize_to_icons. "
            "Set it to True and the menu is shown as icons only, when normally it would be hidden.\n"
            "\n\n"
            "Try this with the 'Minimize to icons' toggle in the top bar."
            "\n\n"
            "There are also landscape_minimize_to_icons and portrait_minimize_to_icons properties that you can "
            "use to set this property differently in each orientation.",
        ),
    ),
    (
        dict(
            icon=icons.COMPARE_ARROWS_OUTLINED,
            selected_icon=icons.COMPARE_ARROWS,
            label="Menu width",
        ),
        create_page(
            "Menu width",
            "ResponsiveMenuLayout has a parameter manu_extended. "
            "Set it to False to place menu labels under the icons instead of beside them."
            "\n\n"
            "Try this with the 'Menu width' toggle in the top bar.",
        ),
    ),
    (
        dict(
            icon=icons.ROUTE_OUTLINED,
            selected_icon=icons.ROUTE,
            label="Route support",
            route="custom-route",
        ),
        create_page(
            "Route support",
            "ResponsiveMenuLayout has a parameter support_routes, which is True by default. "
            "\n\n"
            "Routes are useful only in the web, where the currently selected page is shown in the url, "
            "and you can open the app directly on a specific page with the right url."
            "\n\n"
            "You can specify a route explicitly with a 'route' item in the menu dict (see this page in code). "
            "If you do not specify the route, a slugified version of the page label is used "
            "('Menu width' becomes 'menu-width').",
        ),
    ),
    (
        dict(
            icon=icons.PLUS_ONE_OUTLINED,
            selected_icon=icons.PLUS_ONE,
            label="Fine control",
        ),
        create_page(
            "Adjust navigation rail",
            "NavigationRail is accessible via the navigation_rail attribute of the ResponsiveMenuLayout. "
            "In this demo it is used to add the leading button control."
            "\n\n"
            "These NavigationRail attributes are used by the ResponsiveMenuLayout, and changing them directly "
            "will probably break it:\n"
            "- destinations\n"
            "- extended\n"
            "- label_type\n"
            "- on_change\n",
        ),
    ),
]
