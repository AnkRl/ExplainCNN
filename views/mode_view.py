import flet as ft
import utils

def ModeView(router):
    translator = router.get_data("translator")["mode_view"]
    width, height, vertical, horizontal = utils.get_size_with_margin(0.6,0.4)

    def go_to_camera(e: ft.ControlEvent):
        e.page.go("/camera")

    def go_to_gallery(e: ft.ControlEvent):
        e.page.go("/gallery")
    
    def go_to_random(e:ft.ControlEvent):        
        router.set_data("img_org", router.image_manager.random_image())
        e.page.go("/compare")

    modes = [
        "mode_random", 
        "mode_gallery", 
        "mode_camera"
    ]

    modes_icons = {
        "mode_random": ft.icons.IMAGE,
        "mode_gallery": ft.icons.IMAGE_SEARCH,
        "mode_camera": ft.icons.CAMERA_ALT_ROUNDED,
    }

    modes_handle_click = {
        "mode_random": go_to_random,
        "mode_gallery": go_to_gallery,
        "mode_camera": go_to_camera,
    }

    card_list = [ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(name=modes_icons[mode], color=ft.colors.PRIMARY, size=70),
                                ft.Text(
                                    translator[f"{mode}_title"],
                                    theme_style=ft.TextThemeStyle.TITLE_SMALL
                                ),
                                ft.Text(
                                    translator[f"{mode}_text"],
                                    theme_style = ft.TextThemeStyle.BODY_MEDIUM
                                ),
                                ft.ElevatedButton(translator["button"], on_click=modes_handle_click[mode])
                            ],
                            # Params for content column
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        width = (width*0.9)/3,
                        height = height*0.9,
                        padding=10,
                    ))
        for mode in modes
    ]

    content = ft.Container(
        ft.Container(
            ft.Row(
                card_list,
                # Params for content row
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        # Params for Main content container
        width= width,
        height= height,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),        
        ),
        margin=ft.margin.symmetric(horizontal=horizontal, vertical=vertical),
        alignment=ft.alignment.center,
    )
    
    return content
