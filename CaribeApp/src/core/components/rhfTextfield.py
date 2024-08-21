import flet as ft


class RHFTexField(ft.Container):
    def __init__(
        self,
        /,
        label: str,
        error: str = "",
        helper_text: str = "",
        data=None,
        inputfilter=None,
        onChange=None,
        onBlur=None,
        required=False,
    ):
        self.label = label
        self.onChange = onChange
        self.onBlur = onBlur
        self.error = error
        self.helper_text = helper_text

        ft.Container.__init__(
            self,
            content=ft.Column(
                spacing=1,
                controls=[
                    ft.TextField(
                        autofocus=True,
                        on_change=self.onChange,
                        on_blur=self.onBlur,
                        color="#FF0000" if self.error != "" else None,
                        input_filter=inputfilter,
                        data=data,
                        focused_border_color="#8A0F12",
                        label=(self.label if not required else f"{self.label} *"),
                        error_text=self.error,
                        helper_text=self.helper_text,
                        focused_color="#8A0F12",
                        bgcolor=ft.colors.TRANSPARENT,
                        label_style=ft.TextStyle(
                            size=14,
                            color="",
                        ),
                        height=48,
                        border_color="#f4f4f4",
                    ),
                ],
            ),
        )
