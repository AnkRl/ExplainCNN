import flet as ft

# handling translations
import utils 
translator = utils.translator["mode_view"]

def ModeView(router):

    #TODO: Handle images
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/2")

    def go_to_gallery(e: ft.ControlEvent):
        e.page.go("/gallery")
    
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
        "mode_random": go_to,
        "mode_gallery": go_to_gallery,
        "mode_camera": go_to,
    }

    card_list = [ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Icon(name=modes_icons[mode], color=ft.colors.PRIMARY, size=50),
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
                        width=240,
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
        width= 900,
        height= 300,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),        
        ),
        margin=100,
        alignment=ft.alignment.center,
    )
    
    return content
