import flet as ft
from src.core.components.rhfTextfield import RHFTexField


class FieldClass:
    def __init__(self, name: str, value=None, placeholder: str = None, /) -> None:
        self.name = name
        self.value = value
        self.placeholder = placeholder


class Facultad(ft.Container):
    def __init__(self, /, page: ft.Page, index, colores: list[str], remove: callable):
        self.page = page
        self.init_state()
        self.remove_input = remove
        self.index = index
        self.colores = colores
        self.dropdown = ft.Dropdown(
            label="Color preferido",
            data=self.fields[3].value,
            border_color="#f4f4f4",
            options=colores,
            item_height=32,
            error_text="No hay colores disponibles" if colores.__len__() <= 0 else "",
        )

        ft.Container.__init__(
            self,
            padding=ft.Padding(0, 16, 0, 16),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=16,
                controls=[
                    RHFTexField(
                        label="Nombre de la facultad",
                        error="",
                        data=self.fields[0].value,
                        required=True,
                    ),
                    RHFTexField(
                        label="Posición en el juego pasado",
                        error="",
                        data=self.fields[1].value,
                        required=True,
                    ),
                    RHFTexField(
                        label="Cantidad de deportistas",
                        error="",
                        data=self.fields[2].value,
                    ),
                    self.dropdown,
                    ft.CupertinoButton(
                        text="Eliminar",
                        bgcolor="#8A0F12",
                        icon=ft.cupertino_icons.TRASH,
                        color=(ft.colors.WHITE),
                        data=index,
                        on_click=self.remove_input,
                        col=12,
                    ),
                ],
            ),
        )

    def init_state(self):
        self.fields = [
            FieldClass("Nombre de la facultad"),
            FieldClass("Posición en el juego pasado"),
            FieldClass("Cantidad de deportistas"),
            FieldClass("Color preferido"),
        ]


class Color(ft.Container):
    def __init__(
        self,
        /,
        page: ft.Page,
        index,
        remove: callable,
        on_blur: callable = None,
    ):
        self.page = page
        self.init_state()
        self.remove_input = remove

        def onChange(newValue: ft.ControlEvent, index):
            self.fields[index].value = newValue.data

        ft.Container.__init__(
            self,
            padding=ft.Padding(16, 16, 16, 16),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=16,
                controls=[
                    RHFTexField(
                        label="Nombre del color",
                        error="",
                        data=self.fields[0].value,
                        required=True,
                        onChange=lambda e: onChange(e, 0),
                        inputfilter=ft.TextOnlyInputFilter(),
                        onBlur=on_blur,
                    ),
                    RHFTexField(
                        label="Cantidad de pullovers",
                        error="",
                        data=self.fields[1].value,
                        required=True,
                        onChange=lambda e: onChange(e, 1),
                        inputfilter=ft.NumbersOnlyInputFilter(),
                        onBlur=on_blur,
                    ),
                    ft.CupertinoButton(
                        text="Eliminar",
                        bgcolor="#8A0F12",
                        icon=ft.cupertino_icons.TRASH,
                        color=(ft.colors.WHITE),
                        data=index,
                        on_click=self.remove_input,
                        col=12,
                    ),
                ],
            ),
        )

    def init_state(self):
        self.fields = [
            FieldClass("Nombre del color", ""),
            FieldClass("Cantidad de pullovers", 0),
        ]


class Pullovers(ft.Container):
    def __init__(self, page: ft.Page, /):
        self.page = page
        self.init_state()
        self.colors = []

        def get_colors():
            colors = []
            for color in self.inputs_container_colors.controls:
                colors.append(color.fields[0].value)
            return colors

        def add_new_input_combo(container):
            container.controls.append(
                Facultad(
                    page=self.page,
                    index=container.controls.__len__(),
                    colores=[
                        ft.dropdown.Option(key=color, text=color)
                        for color in get_colors()
                        if color
                    ],
                    remove=lambda e: {
                        container.controls.remove(container.controls[e.control.data]),
                        container.update(),
                    },
                )
            )
            self.update()

        def update_colors_of_facultades():
            print("update_colors_of_facultades")
            colores = get_colors()

            for facultad in self.inputs_container_pullovers.controls:
                facultad.dropdown.options = [
                    ft.dropdown.Option(key=color, text=color)
                    for color in colores
                    if color
                ]
                facultad.dropdown.error_text = (
                    "No hay colores disponibles"
                    if facultad.dropdown.options.__len__() <= 0
                    else ""
                )
                facultad.update()

            self.update()

        def add_new_input_combo_color(container):
            container.controls.append(
                Color(
                    page=self.page,
                    index=container.controls.__len__(),
                    remove=lambda e: {
                        container.controls.remove(container.controls[e.control.data]),
                        container.update(),
                    },
                    on_blur=lambda e: update_colors_of_facultades(),
                )
            )
            self.update()

        self.inputs_container_colors = ft.Column(
            controls=[],
        )

        self.inputs_container_pullovers = ft.Column(
            controls=[],
        )

        ft.Container.__init__(
            self,
            padding=ft.Padding(16, 16, 16, 16),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=16,
                controls=[
                    RHFTexField(
                        label="Cantidad de pullovers",
                        error="",
                        data=self.fields[0].value,
                        required=True,
                    ),
                    RHFTexField(
                        label="Cantidad para árbitros y profesores",
                        error="",
                        data=self.fields[1].value,
                    ),
                    RHFTexField(
                        label="Cantidad para antiguos atletas",
                        error="",
                        data=self.fields[2].value,
                    ),
                    ft.Divider(color=ft.colors.BLACK12),
                    self.inputs_container_colors,
                    ft.CupertinoButton(
                        text="Nuevo color",
                        bgcolor="#8A0F12",
                        color=(ft.colors.WHITE),
                        on_click=lambda _: add_new_input_combo_color(
                            self.inputs_container_colors
                        ),
                        col=12,
                    ),
                    ft.Divider(color=ft.colors.BLACK12),
                    self.inputs_container_pullovers,
                    ft.CupertinoButton(
                        text="Nueva facultad",
                        bgcolor="#8A0F12",
                        color=(ft.colors.WHITE),
                        on_click=lambda _: add_new_input_combo(
                            self.inputs_container_pullovers
                        ),
                        col=12,
                    ),
                ],
            ),
        )

    def init_state(self):
        self.fields = [
            FieldClass("Cantidad de pullovers"),
            FieldClass("Cantidad para árbitros y profesores"),
            FieldClass("Cantidad para antiguos atletas"),
        ]
