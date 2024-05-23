
import flet as ft
import flet.canvas as cv
import utils
import time

class State:
    x: float
    y: float
state = State()

# handling translations

class ai_overlay(ft.UserControl):
    def __init__(self, router, go_to):
        super().__init__()
        self.router = router
        self.isolated = True
        self.go_to = go_to
        self.translator = router.get_data("translator")["compare_view"]

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
                        self.translator["button"], 
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
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
        return content

def CompareView(router):
    translator = router.get_data("translator")["compare_view"]
    router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    #ki_image = router.image_manager.ki_image

    width, height, vertical, horizontal = utils.get_size_with_margin(0.8,0.8)
    SIZE_CANVAS_X = (width*0.9)*0.5
    SIZE_CANVAS_Y = (height*0.9)*0.5

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
                    state.x, state.y, e.local_x, e.local_y, paint=ft.Paint(color = "#0000ff", stroke_width=3)
                ) 
            )
            cp.update()
            state.x = e.local_x
            state.y = e.local_y
    
    cp = cv.Canvas([],
        width=SIZE_CANVAS_X,
        height= SIZE_CANVAS_Y,
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
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
                    ft.Stack([                        
                        ft.Image(
                            src=router.get_data("img_org"),
                            height = SIZE_CANVAS_Y,
                            width = SIZE_CANVAS_X,
                        ),
                        cp
                    ])
                ],
                # Params for content column
                #TODO: Width?
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

    row_ai = ft.Container(
                    ft.Column([
                        ft.TextField(
                            label=translator["user_input"], 
                            icon=ft.icons.COMPUTER, 
                            read_only=True,
                        ),
                        ft.Text(
                            translator[f"user_text"],
                            theme_style = ft.TextThemeStyle.BODY_MEDIUM,
                        ),
                        ft.Image(
                            src=router.get_data("img_org"),
                            height = SIZE_CANVAS_Y,
                            width = SIZE_CANVAS_X,
                        ),
                        
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                width=(width*0.9)/2,
                height=height*0.9,
                alignment=ft.alignment.center
            )
    
    ao = ai_overlay(router=router, go_to=go_to)
    
    overlay_ai = ft.Container(
                        ao,
                        width=(width*0.91)/2,
                        height=height*0.91,
                        alignment=ft.alignment.center,
                        blur=ft.Blur(2,2,ft.BlurTileMode.MIRROR),
                    )
    
    content =      ft.Row([
                        # User
                        ft.Container(
                            row_user,
                            width=(width*0.9)/2,
                            height=height*0.9,
                            alignment=ft.alignment.center
                        ),                
                        #AI
                        ft.Container(
                            ft.Stack([
                                row_ai,
                                overlay_ai
                            ]),
                            width=(width*0.9)/2,
                            height=height*0.9,
                            alignment=ft.alignment.center
                        )
                    ],
                        # # Params for content row
                        # width=(width*0.9),
                        # height=height*0.9,
                        # alignment=ft.MainAxisAlignment.CENTER,
                        # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
    
    return content
