from typing import Union
import flet as ft
from views.Router import Router, DataStrategyEnum
from State import global_state, State

# handling translations
import utils 
translator = utils.translator["start_view"]

def StartView(router_data: Union[Router, str, None] = None):

    #TODO: Load everything in the background!
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/1")

    title = ft.Text(
        translator["title"],
        color="white",
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL
    )
    text = ft.Text(
        translator["text"],
        color="white",
        theme_style = ft.TextThemeStyle.BODY_MEDIUM
    )
    start_button = ft.ElevatedButton(translator["button"])
    start_button.on_click = go_to


    content = ft.Container(
        ft.Container(
        ft.Column([
            title,
            text,
            start_button
        ],
        # Params for content column
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        # Params for Main content container
        width= 600,
        height= 600,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),   
        
        ),
        margin=100,
        alignment=ft.alignment.center,
    )
    
    return content