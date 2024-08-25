import flet as ft
from src.core.components.rhfTextfield import RHFTexField
from src.PuLP_Solver import PuLP_Solver


class colorClass:
    def __init__(self, name, cantidad):
        self.name = name
        self.cantidad = cantidad


class facultadClass:
    def __init__(self, name, last_position, sport_men, color):
        self.name = name
        self.last_position = last_position
        self.sport_men = sport_men
        self.color = color


class FieldClass:
    def __init__(
        self,
        name: str,
        cast: callable,
        value=None,
        /,
        placeholder: str = None,
        required=True,
    ) -> None:
        self.name = name
        self.value = value
        self.required = required
        self.placeholder = placeholder
        self.cast = cast


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
            error_text="No hay colores disponibles" if colores.__len__() <= 0 else "",
            on_change=lambda x: onChange(x, 3),
        )

        def onChange(newValue: ft.ControlEvent, index):
            self.fields[index].value = self.fields[index].cast(newValue.data)

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
                        required=self.fields[0].required,
                        onChange=lambda x: onChange(x, 0),
                    ),
                    RHFTexField(
                        label="Posición en el juego pasado",
                        error="",
                        data=self.fields[1].value,
                        required=self.fields[1].required,
                        onChange=lambda x: onChange(x, 1),
                        inputfilter=ft.NumbersOnlyInputFilter(),
                        keyboard=ft.KeyboardType.NUMBER,
                    ),
                    RHFTexField(
                        label="Cantidad de deportistas",
                        error="",
                        data=self.fields[2].value,
                        onChange=lambda x: onChange(x, 2),
                        required=self.fields[2].required,
                        inputfilter=ft.NumbersOnlyInputFilter(),
                        keyboard=ft.KeyboardType.NUMBER,
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
            FieldClass("Nombre de la facultad", lambda x: str(x)),
            FieldClass("Posición en el juego pasado", lambda x: int(x)),
            FieldClass("Cantidad de deportistas", lambda x: int(x), required=False),
            FieldClass(
                "Color preferido",
                lambda x: str(x),
                required=False,
            ),
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
            self.fields[index].value = self.fields[index].cast(newValue.data)

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
                        keyboard=ft.KeyboardType.NUMBER,
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
            FieldClass("Nombre del color", lambda x: str(x)),
            FieldClass("Cantidad de pullovers", lambda x: int(x)),
        ]


class CardAnswerContainer(ft.Card):
    def __init__(self, name, value):
        text = name + " " + value[0] + " " + value[1]
        print(text)
        ft.Card.__init__(
            self,
            content=ft.Container(
                padding=[4, 4, 4, 4],
                content=ft.Text("text"),
            ),
            elevation=1,
        )


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
            update_colors_of_facultades()

        def onChange(newValue: ft.ControlEvent, index):
            self.fields[index].value = self.fields[index].cast(newValue.data)

        def update_colors_of_facultades():
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

        self.ans_container = ft.Column(controls=[])

        def execute_bk():
            self.page.window_progress_bar = ft.ProgressBar(color=ft.colors.GREEN_500)

            self.page.update()

            incomplete_data = False
            if not self.fields[0] or not self.fields[1]:
                incomplete_data = True
                print(self.fields[0].name, " ", self.fields[0].value)
                print(self.fields[1].name, " ", self.fields[1].value)

            colors: list[colorClass] = []
            for i in self.inputs_container_colors.controls:
                i: Color

                for f in i.fields:
                    if f.required and not f.value:
                        incomplete_data = True
                        print(f.name, " ", f.value)

                if not incomplete_data:
                    colors.append(colorClass(*[v.value for v in i.fields]))

            facultades: list[facultadClass] = []
            for i in self.inputs_container_pullovers.controls:
                for f in i.fields:
                    if f.required and not f.value:
                        incomplete_data = True
                        print(f.name, " ", f.value)

                if not incomplete_data:
                    facultades.append(facultadClass(*[v.value for v in i.fields]))

            if incomplete_data:
                print("+++++++++++++++++++ DATA INCOMPLETA ++++++++++++++++++++")
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Revise los datos, existen campos vacíos"),
                    action="Cerrar",
                )
                page.snack_bar.open = True
                page.update()

            else:
                facultades_name = [f.name for f in facultades]
                athletes_dict: dict = {}
                ranking_dict: dict = {}
                favorite_colors_dict: dict = {}
                colors_dict: dict = {}

                for f in facultades:
                    athletes_dict[f.name] = f.sport_men
                    ranking_dict[f.name] = f.last_position
                    favorite_colors_dict[f.name] = f.color

                for c in colors:
                    colors_dict[c.name] = c.cantidad

                print("=============================================")
                print("Nombre de las facultades")
                print(facultades_name)
                print("Atletas")
                print(athletes_dict)
                print("Colors")
                print(colors_dict)
                print("")
                print("=============================================")
                try:
                    ans = PuLP_Solver(
                        facultades_name,
                        athletes_dict,
                        ranking_dict,
                        colors_dict,
                        self.fields[0].value,
                        self.fields[1].value,
                        favorite_colors_dict,
                    )
                    print("fin del request")
                    print(ans.assigned_pullovers)
                    parse_data = []
                    for ans in ans.assigned_pullovers.items():
                        parse_data.append([str(ans[0]), str(ans[1])])
                        print(parse_data)

                    self.ans_container.controls = [
                        CardAnswerContainer(name=i[0], value=i[1]) for i in parse_data
                    ]
                    self.ans_container.update()

                except Exception as e:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text(e),
                        action="Cerrar",
                    )
                    page.snack_bar.open = True

                page.update()

            self.page.window_progress_bar = None
            self.page.update()

        ft.Container.__init__(
            self,
            padding=ft.Padding(24, 24, 24, 24),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
                spacing=16,
                controls=[
                    RHFTexField(
                        label="Cantidad para árbitros y profesores",
                        error="",
                        data=self.fields[0].value,
                        onChange=lambda x: onChange(x, 0),
                        required=True,
                        inputfilter=ft.NumbersOnlyInputFilter(),
                        keyboard=ft.KeyboardType.NUMBER,
                    ),
                    RHFTexField(
                        label="Cantidad para antiguos atletas",
                        error="",
                        data=self.fields[1].value,
                        onChange=lambda x: onChange(x, 1),
                        required=True,
                        inputfilter=ft.NumbersOnlyInputFilter(),
                        keyboard=ft.KeyboardType.NUMBER,
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
                    ft.Row(
                        controls=[
                            ft.FloatingActionButton(
                                bgcolor="#8A0F12",
                                col=12,
                                icon=ft.cupertino_icons.PLAY,
                                foreground_color=ft.colors.WHITE,
                                on_click=lambda _: execute_bk(),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    self.ans_container,
                ],
            ),
        )

    def init_state(self):
        self.fields = [
            FieldClass("Cantidad para árbitros y profesores", lambda x: int(x)),
            FieldClass("Cantidad para antiguos atletas", lambda x: int(x)),
        ]
