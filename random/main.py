import flet as ft
import random


def main(page: ft.Page):
    page.title = "CaribeApp"
    page.scroll = ft.ScrollMode.HIDDEN

    page.theme_mode = ft.ThemeMode.LIGHT

    tmp = ["1", "2", "3", "4"]
    text = tmp[0]

    def random_v(_text):

        _text = random.choice(tmp)
        page.update()

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.add(ft.ElevatedButton(text="tocame", on_click=lambda _: random_v(text)))
    page.add(ft.Text(text))
    page.update()


ft.app(target=main)
