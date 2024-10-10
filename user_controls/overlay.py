import flet as ft
import utils

def Overlay(router):    
    translator = router.get_data("translator")["start_view"]
    width, height = utils.get_size_main_container()

    
    content = ft.Column(
                    [
                        ft.Image(src="",
                             width=(width*0.9)/3
                            ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return content