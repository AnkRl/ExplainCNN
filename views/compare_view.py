
import flet as ft
import flet.canvas as cv
import utils

class State:
    x: float
    y: float
state = State()

# handling translations

import utils 
translator = utils.translator["compare_view"]
SIZE_CANVAS_X = 250
SIZE_CANVAS_Y = 250


def CompareView(router):

    router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    ki_image = router.image_manager.ki_image

    def out_of_boundary(e: ft.DragUpdateEvent):
        size_x, size_y = SIZE_CANVAS_X,SIZE_CANVAS_Y
        pos_x, pos_y = 0,0
        x = e.local_x
        y = e.local_y
        
        if x > pos_x and x < size_x + pos_x and y > pos_y and y < size_y + pos_y:
            return False
        else:
            return True
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/mode")

    def pan_start(e: ft.DragStartEvent):
        state.x = e.local_x
        state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        if out_of_boundary(e):
            pass
        else:
            cp.shapes.append(
                cv.Line(
                    state.x, state.y, e.local_x, e.local_y, paint=ft.Paint(color = utils.IMAGE_YELLOW, stroke_width=3)
                ) 
            )
            cp.update()
            state.x = e.local_x
            state.y = e.local_y

    cp = cv.Canvas([],
        width=250,
        height= 250,
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
            width=250,
            height= 250,
        ),
    )

    row_user = ft.Column([
                    ft.TextField(label=translator["user_input"], icon=ft.icons.PERSON_ROUNDED),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM
                    ),
                        ft.Container(
                            cp,
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            image_src=router.get_data("img_org"),
                    )
                    #ft.ElevatedButton(translator["button"], on_click=go_to)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    row_ai = ft.Column([
                    ft.TextField(value = router.image_manager.prediction, label=translator["user_input"], icon=ft.icons.COMPUTER, read_only=True),
                    ft.Text(
                        translator[f"user_text"],
                        theme_style = ft.TextThemeStyle.BODY_MEDIUM
                    ),
                    ft.Image(
                        src_base64=ki_image
                    )
                    #ft.ElevatedButton(translator["button"], on_click=go_to)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
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