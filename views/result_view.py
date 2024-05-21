
import flet as ft
import flet.canvas as cv
import utils
from assets.categories import *

class State:
    x: float
    y: float
state = State()

# handling translations
SIZE_CANVAS_X = 250
SIZE_CANVAS_Y = 250


def ResultView(router):
    translator = router.get_data("translator")["compare_view"]
    #router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    ki_image = router.image_manager.ki_image
    curr_lng = router.get_data("lng")
    categories = de_categories() if curr_lng is "DE" else en_categories()
    ai_guess = categories[router.image_manager.prediction]

    def out_of_boundary(e: ft.DragUpdateEvent):
        size_x, size_y = SIZE_CANVAS_X,SIZE_CANVAS_Y
        pos_x, pos_y = 0,0
        x = e.local_x
        y = e.local_y
        
        if x > pos_x and x < size_x + pos_x and y > pos_y and y < size_y + pos_y:
            return False
        else:
            return True

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
                            width = 350,
                            height = 350,
                            alignment=ft.alignment.center,
                            image_src=router.get_data("img_org"),
                    )
                    #ft.ElevatedButton(translator["button"], on_click=go_to)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    row_ai = ft.Column([
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
                        width=350,
                        height = 350,
                    )
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                #horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    content = ft.Container(
        ft.Container(
            ft.Row([
                # User
                row_user,
                #AI
                row_ai
            ],
                # Params for content row
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        # Params for Main content container
        width= 900,
        height= 700,
        border_radius= 18,
        border= ft.border.all(1, "#44f4f4f4"),
        alignment=ft.alignment.center,
        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR),        
        ),
        margin=100,
        alignment=ft.alignment.center,
    )
    
    
    return content
