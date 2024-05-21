import flet as ft
import json
import utils

def LanguageView(router):
    width, height, vertical, horizontal = utils.get_size_with_margin(0.6,0.4)

    def switch_lng(lng):
        match lng:
            case "DE":
                file = "assets/de.json"
            case "EN" | _:
                file = "assets/en.json"
        with open(file, "rb") as f:
            text = json.load(f)
        router.set_data("translator", text)
        router.set_data("lng", lng)
            
    
    def click(e: ft.ControlEvent):
        switch_lng(e.control.data)
        e.page.go("/start")

    curr_lng = router.get_data("lng")

    content = ft.Container(
        ft.Container(
        ft.Column([
            ft.ListTile(
                            title=ft.Text("Deutsch"),
                            data="DE",
                            on_click= click,
                            selected = True if curr_lng is "DE" else False,
                        ),
            ft.ListTile(
                            title=ft.Text("English"),
                            data ="EN",
                            on_click = click,
                            selected = True if curr_lng is "EN" else False,
                        ),
        ],
        # Params for content column
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        # Params for Main content container
        width= width,
        height= height,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),   
        
        ),
        margin= ft.margin.symmetric(horizontal=horizontal, vertical=vertical),
        alignment=ft.alignment.center,
    )
    return content