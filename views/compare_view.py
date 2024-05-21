
import flet as ft
import flet.canvas as cv
import utils
import time

class State:
    x: float
    y: float
state = State()

# handling translations

import utils 
translator = utils.translator["compare_view"]
SIZE_CANVAS_X = 250
SIZE_CANVAS_Y = 250

class ai_overlay(ft.UserControl):
    def __init__(self, router, go_to):
        super().__init__()
        self.router = router
        self.isolated = True
        self.go_to = go_to

    def did_mount(self):
        self.update_timer()
        self.button.disabled = False
        self.update()

    def update_timer(self):
        for i in range(0, 101):
            self.progress.value = i * 0.01
            time.sleep(0.05)
            self.update()
        

    def build(self):
        self.button =ft.ElevatedButton(
                        translator["button"], 
                        disabled = True, 
                        on_click=self.go_to)
        self.progress = ft.ProgressRing(
            width=50, 
            height=50, 
            stroke_width = 2,
            value = 0.1)
        
        content = ft.Column([
                    self.progress,
                    self.button
                    ])
        return content

def CompareView(router):
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
        router.set_data("canvas", cp)
        e.page.go("/result")

    def on_change_input (e: ft.ControlEvent):
        router.set_data("user_guess", e.data)

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
                    ft.TextField(
                        label=translator["user_input"], 
                        icon=ft.icons.PERSON_ROUNDED,
                        on_change = on_change_input,
                        ),
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

    row_ai = ft.Column([ ai_overlay(router=router, go_to=go_to)
                    # ft.ElevatedButton(
                    #     translator["button"], 
                    #     disabled = show_ai_image, 
                    #     on_click=go_to)
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
