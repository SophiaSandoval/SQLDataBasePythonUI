import flet as ft


def IndexView(page):
    content = ft.Column(
        [
            ft.Row(
                [ft.Text("", size=50)],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]
    )

    return content
