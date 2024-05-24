import flet as ft
import utils

def NavBar(page):

    CupBar = ft.CupertinoNavigationBar(
        bgcolor = ft.colors.with_opacity(0.5, utils.IMAGE_ORANGE), #ft.colors.AMBER_100,
        inactive_color = ft.colors.with_opacity(0.9, utils.IMAGE_ORANGE_LIGHT),
        active_color=ft.colors.with_opacity(0.9, utils.IMAGE_ORANGE_DARK),
        on_change = lambda e: page.go(f"/{e.control.selected_index}"),
        destinations = [
            ft.NavigationDestination(icon=ft.icons.HOME_ROUNDED),
            ft.NavigationDestination(icon=ft.icons.IMAGE_SEARCH_ROUNDED),
            ft.NavigationDestination(icon=ft.icons.LANGUAGE),
        ]
    )

    return CupBar
