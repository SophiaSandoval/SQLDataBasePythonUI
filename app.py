import flet as ft


def NavBar(page, ft=ft):
    NavBar = ft.AppBar(
        leading=ft.Icon(ft.icons.TAG_FACES_ROUNDED),
        leading_width=40,
        title=ft.Text("Books DataBase"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    return NavBar
