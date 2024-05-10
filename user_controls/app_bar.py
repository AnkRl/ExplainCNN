import flet as ft
import utils
from enum import Enum

def NavBar(page):
    NavBar = ft.AppBar(
            leading=ft.Icon(ft.icons.TAG_FACES_ROUNDED),
            leading_width=40,
            title=ft.Text("Flet Router"),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.IconButton(ft.icons.HOME, on_click=lambda _: page.go('/')),
                ft.IconButton(ft.icons.PERSON_ROUNDED, on_click=lambda _: page.go('/profile')),
                ft.IconButton(ft.icons.SETTINGS_ROUNDED, on_click=lambda _: page.go('/settings'))
            ]
        )
    
    CupBar = ft.CupertinoNavigationBar(
        bgcolor = ft.colors.with_opacity(0.5, utils.IMAGE_ORANGE), #ft.colors.AMBER_100,
        #inactive_color = ft.colors.with_opacity(0.9, utils.IMAGE_YELLOW),
        #active_color=ft.colors.with_opacity(0.9, utils.IMAGE_YELLOW),
        on_change = lambda e: page.go(f"/{e.control.selected_index}"),
        destinations = [
            ft.NavigationDestination(icon=ft.icons.EXPLORE, label="Explore"),
            ft.NavigationDestination(icon=ft.icons.COMMUTE, label="Commute"),
            ft.NavigationDestination(
                icon=ft.icons.BOOKMARK_BORDER,
                selected_icon=ft.icons.BOOKMARK,
                label="Explore",
            ),
        ]
    )

    return CupBar
