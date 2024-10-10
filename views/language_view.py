import flet as ft
import json
import utils

def LanguageView(router):
    width, height = utils.get_size_main_container()  

    def switch_lng(lng):
        if lng is "DE":
            file = "assets/de.json"
        else:
            file = "assets/en.json"
        
        with open(file, "rb") as f:
            text = json.load(f)
        router.set_data("translator", text)
        router.set_data("lng", lng)            
    
    def click(e: ft.ControlEvent):
        switch_lng(e.control.data)
        e.page.go("/start")

    curr_lng = router.get_data("lng")

    content = ft.Column(
        [
            ft.Image(src="assets/language.svg", width=width*0.2),
            ft.TextButton(
                "Deutsch",
                data="DE",
                on_click= click,
                icon = "check" if curr_lng == "DE" else None,
                ),
            ft.TextButton(
                "English",
                data="EN",
                on_click= click,
                icon = "check" if curr_lng == "EN" else None,
                ),
            ft.Text("Illustrations by Storyset.com", color="white")
        ],
        width=width,
        height=height,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    return content