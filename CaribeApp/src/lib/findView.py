from flet import View, Page


def find_view(page: Page) -> View:
    for view in page.views:
        if view.route == page.route:
            return view
    return None
