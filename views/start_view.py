import flet as ft
import utils

def StartView(router):    
    translator = router.get_data("translator")["start_view"]
    width, height = utils.get_size_main_container()
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/mode")

    image = ft.Image(
        src = "assets/start.svg",
        width=width*0.6,
    )
    title = ft.Text(
        translator["title"],
        color= ft.colors.SECONDARY,#"white",
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
                        image,
                        title,
                        text,
                        start_button
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    
                    )
    
    return content