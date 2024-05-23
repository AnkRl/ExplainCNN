
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
    #router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    ki_image = router.image_manager.ki_image
    curr_lng = router.get_data("lng")
    categories = de_categories() if curr_lng is "DE" else en_categories()
    ai_guess = categories[router.image_manager.prediction]

    width, height, vertical, horizontal = utils.get_size_with_margin(0.8,0.8)
    SIZE_CANVAS_X = (width*0.9)*0.5
    SIZE_CANVAS_Y = (height*0.9)*0.5

    cp = router.get_data("canvas")

    row_user = ft.Column([
                    ft.TextField(
                        label=translator["user_input"], 
                        icon=ft.icons.PERSON_ROUNDED,
                        value = router.get_data("user_guess"),
                        read_only=True),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM
                    ),
                        ft.Container(
                            cp,
                            width = SIZE_CANVAS_X,
                            height = SIZE_CANVAS_Y,
                            alignment=ft.alignment.center,
                            image_src=router.get_data("img_org"),
                    )
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    row_ai = ft.Container(
                ft.Column([
                    ft.TextField(
                        value = ai_guess, 
                        label=translator["user_input"], 
                        icon=ft.icons.COMPUTER, 
                        read_only=True,
                    ),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM,
                    ),
                    ft.Image(
                        src_base64=ki_image ,
                        width=SIZE_CANVAS_X,
                        height = SIZE_CANVAS_Y,
                    )
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=(width*0.9)/2,
                height=height*0.9,
                alignment=ft.alignment.center
            )
    
    content = ft.Container(
        ft.Container(
            ft.Row([
                # User
                ft.Container(
                    row_user,
                    width=(width*0.9)/2,
                    height=height*0.9,
                    alignment=ft.alignment.center
                ),                
                #AI
                ft.Container(
                    row_ai,
                    width=(width*0.9)/2,
                    height=height*0.9,
                    alignment=ft.alignment.center
                )
            ],
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
