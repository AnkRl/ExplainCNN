import flet as ft
import json
import utils

def LanguageView(router):
    width, height = utils.get_size_main_container()  

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

    

    lang = ft.Column([
            ft.ListTile(
                            title=ft.Text("Deutsch"),
                            data="DE",
                            on_click= click,
                            selected = True if curr_lng is "DE" else False,
                            bgcolor="white"
                        ),
            ft.ListTile(
                            title=ft.Text("English"),
                            data ="EN",
                            on_click = click,
                            selected = True if curr_lng is "EN" else False,
                            bgcolor=ft.colors.GREEN_100,
                        ),
        ],
        # Params for content column
        width= width*0.5,
        height= height*0.3,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    content = ft.Column(
        [
            ft.Image(src="assets/language.svg", width=width*0.2),
            ft.TextButton(
                "Deutsch",
                data="DE",
                on_click= click,
                icon = "check" if curr_lng is "DE" else None,
                ),
            ft.TextButton(
                "English",
                data="EN",
                on_click= click,
                icon = "check" if curr_lng is "EN" else None,
                ),
            ft.Text("Illustrations by Storyset.com", color="white")
        ],
        width=width,
        height=height,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return content