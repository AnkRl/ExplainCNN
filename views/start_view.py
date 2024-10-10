import flet as ft
import utils

def StartView(router):    
    translator = router.get_data("translator")["start_view"]
    width, height = utils.get_size_main_container()
    
    def go_to_explain(e: ft.ControlEvent):
        router.set_data("flag", "EXPLAIN")
        e.page.go("/choose_image")

    def go_to_attack(e: ft.ControlEvent):
        router.set_data("flag", "ATTACK")
        e.page.go("/choose_image")

    modes = [
        "mode_explain", 
        "mode_attack"
    ]

    modes_images = {
        "mode_explain": "assets/explain.gif",
        "mode_attack": "assets/attack.gif",
    }

    modes_handle_click = {
        "mode_explain": go_to_explain,
        "mode_attack": go_to_attack,
    }

    card_list = [ft.GestureDetector(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.Image(src=modes_images[mode],
                                             width=(width*0.9)/3
                                             ),
                                    ft.Text(
                                        translator[f"{mode}_title"],
                                        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                                        color="white"
                                    )
                                ],
                                # Params for content column
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            width = (width*0.9)/3,
                            height = height*0.9,
                            padding=10,
                        ),
                    on_tap= modes_handle_click[mode],
                )

        for mode in modes
    ]

    content = ft.Row(
                card_list,
                # Params for content row
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=40
            )
    
    return content