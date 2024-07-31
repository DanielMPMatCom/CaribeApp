from enum import Enum
from flet import Row, Column, Card, Text, Container, cupertino_icons


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
            icon=cupertino_icons.COMMAND,
            selected_icon=cupertino_icons.COMMAND,
            label="Pullovers",
        ),
        create_page(
            "Pullovers",
            "This is the pullovers container",
        ),
    ),
    (
        dict(
            icon=cupertino_icons.QUESTION_CIRCLE,
            selected_icon=cupertino_icons.QUESTION_CIRCLE,
            label="Manual de usuario",
        ),
        create_page("Questions and Answer", "Everything about the app"),
    ),
]
