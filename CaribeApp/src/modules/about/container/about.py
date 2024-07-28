import flet as ft


class About(ft.Container):
    def __init__(self, /):
        ft.Container.__init__(
            self,
            content=ft.Text("About"),
        )
