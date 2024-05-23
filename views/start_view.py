import flet as ft
import utils

def StartView(router):    
    translator = router.get_data("translator")["start_view"]

    width, height, vertical, horizontal = utils.get_size_with_margin(0.6,0.6)
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/mode")

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

    content = ft.Column([
                        title,
                        text,
                        start_button
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
    
    return content