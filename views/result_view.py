
import flet as ft
import flet.canvas as cv
import utils
from assets.categories import *

class State:
    x: float
    y: float
state = State()

def ResultView(router):
    translator = router.get_data("translator")["compare_view"]
    router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    ki_image = router.image_manager.ki_image
    curr_lng = router.get_data("lng")
    categories = de_categories() if curr_lng is "DE" else en_categories()
    ai_guess = categories[router.image_manager.prediction]

    # Calculate widths
    width, height = utils.get_size_main_container()    
    max_size_image = width/3
    half_box = width*0.5
    size_user = width*0.15
    size_ai = width*0.14
    
    def goto(e):
        e.page.go("/mode")

    cp = router.get_data("canvas")

    row_user =  ft.Container(
                    ft.Column([
                        ft.TextField(
                            label=translator["user_input"],
                            value = router.get_data("user_guess"),
                            width=max_size_image,
                            read_only=True,
                            border_color="white",
                            color="white",
                            label_style=ft.TextStyle(color="white")
                            ),
                        ft.Text(
                            translator[f"user_text"],
                            theme_style = ft.TextThemeStyle.BODY_LARGE,
                            color="white"
                        ),
                        ft.Container(
                                cp,
                                width = max_size_image,
                                height = max_size_image,
                                alignment=ft.alignment.center,
                                image_src=router.get_data("img_org"),
                        )
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=half_box,
                alignment=ft.alignment.center_right,
            )

    row_ai = ft.Container(
                ft.Column([
                    ft.TextField(
                        value = ai_guess, 
                        label=translator["user_input"],
                        read_only=True,
                        width=max_size_image,
                        border_color="white",
                        color="white",
                        label_style=ft.TextStyle(color="white")
                    ),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_LARGE,
                        color="white"
                    ),
                    ft.Image(
                        src_base64=ki_image ,
                        width = max_size_image,
                        height = max_size_image,
                    )
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=half_box,
                alignment=ft.alignment.center_left
            )
    
    content = ft.Stack([
                ft.Row([
                    # User
                    ft.Stack(
                        [ft.Image(
                            src = "assets/user.svg",
                            width = size_user,
                            top=0,
                            left = 10),
                        row_user]
                    ),                
                    #AI
                    ft.Stack([                                
                        row_ai,
                        ft.Image(
                                src = "assets/ai.svg",
                                width = size_ai,
                                top=0,
                                right=10),
                    ]),
                ],
                    # Params for content row
                    width=width,
                    height=height,
                    alignment=ft.MainAxisAlignment.CENTER,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.IconButton(icon = ft.icons.AUTORENEW_ROUNDED, icon_size= 85,on_click=goto, bottom = 0, left = width*0.47)])
    
    return content
