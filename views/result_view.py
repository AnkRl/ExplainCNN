
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
    ki_image = router.image_manager.ki_image
    curr_lng = router.get_data("lng")
    categories = de_categories() if curr_lng is "DE" else en_categories()
    
    labels = []
    for i in range(3):
        guess = categories[router.image_manager.prediction[i]]
        prob = round(router.image_manager.probs[i],1)
        labels.append(f"{guess} ({prob}%)")

    # Calculate widths
    width, height = utils.get_size_main_container()    
    max_size_image = width/3
    half_box = width*0.5
    size_user = width*0.15
    size_ai = width*0.14
    
    def goto(e):
        e.page.go("/start")

    cp = router.get_data("canvas")

    row_user =  ft.Container(
                    ft.Column([
                        ft.Row(router.get_data("chips"), width= max_size_image),
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

    def dummy(e):
        pass
    ai_guess = []
    ai_guess.append(
        ft.Chip(
                label=ft.Text(labels[-1]),
                bgcolor=utils.IMAGE_YELLOW,
                autofocus=True,
                selected= True,
                on_select=dummy
            )
    )
    for a in labels[:2]:
        ai_guess.append(
            ft.Chip(
                label=ft.Text(a),
                bgcolor=utils.IMAGE_YELLOW,
                autofocus=True,
                selected= False,
                on_select=dummy,
            )
        )
    row_ai = ft.Container(
                ft.Column([
                    ft.Row(ai_guess, width= max_size_image),
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
                ft.IconButton(
            	    icon = ft.icons.CACHED_ROUNDED, 
                    icon_size= 70,
                    on_click=goto,
                    style=ft.ButtonStyle(color={"": ft.colors.SECONDARY}),
                    bottom = 0, 
                    left = width*0.47)
            ],
            )
    return content
