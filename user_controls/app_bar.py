import flet as ft
import utils

def NavBar(page):

    CupBar = ft.CupertinoNavigationBar(
        bgcolor = ft.colors.with_opacity(0.5, utils.IMAGE_ORANGE), #ft.colors.AMBER_100,
        inactive_color = ft.colors.with_opacity(0.9, utils.GREY_LIGHT),
        active_color=ft.colors.with_opacity(0.9, utils.GREY_DARK),
        on_change = lambda e: page.go(f"/{e.control.selected_index}"),
        destinations = [
            ft.NavigationDestination(icon=ft.icons.HOME_ROUNDED),
            ft.NavigationDestination(icon=ft.icons.LANGUAGE),
        ]
    )

    return CupBar
    rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            height=page.height,
            min_width=100,
            min_extended_width=400,
            #leading=ft.FloatingActionButton(icon=ft.icons.IMAGE_SEARCH_ROUNDED, text="Add"),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED, selected_icon=ft.icons.HOME_ROUNDED, label="First"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.IMAGE_SEARCH_OUTLINED, selected_icon=ft.icons.IMAGE_SEARCH_ROUNDED, label="First"
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.LANGUAGE_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.LANGUAGE_ROUNDED),
                    label="Second",
                ),
            ],
            on_change=lambda e: page.go(f"/{e.control.selected_index}"),
        )
        
    return rail
