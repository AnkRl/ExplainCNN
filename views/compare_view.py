
import flet as ft
import flet.canvas as cv
import utils
import time

class State:
    x: float
    y: float
state = State()

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
    #router.image_manager.get_prediction()
    #router.image_manager.ki_image.save("ki_image.png")
    #ki_image = router.image_manager.ki_image

    # Calculate widths
    width, height = utils.get_size_main_container()    
    max_size_image = width/3
    print(f"Max: {max_size_image}")
    half_box = width*0.5
    size_user = width*0.15
    size_ai = width*0.14

    def out_of_boundary(e: ft.DragUpdateEvent):
        size_x, size_y = max_size_image,max_size_image
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
        width=max_size_image,
        height= max_size_image,
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
    )

    row_user = ft.Container(
                    ft.Column([
                        ft.TextField(
                            label=translator["user_input"],
                            on_change = on_change_input,
                            width=max_size_image,
                            border_color="white",
                            color="white",
                            label_style=ft.TextStyle(color=utils.IMAGE_ORANGE_DARK)
                            ),
                        ft.Text(
                            translator[f"user_text"],
                            theme_style = ft.TextThemeStyle.BODY_LARGE,
                            color="white"
                            ),                    
                        ft.Stack([                        
                            ft.Image(
                                src=router.get_data("img_org"),
                                height = max_size_image,
                                width = max_size_image,
                            ),
                            cp
                        ])
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
                            label=translator["user_input"],
                            read_only=True,
                            width=max_size_image,
                            border_color="white",
                            color="white"
                        ),
                        ft.Text(
                            translator[f"user_text"],
                            theme_style = ft.TextThemeStyle.BODY_LARGE,
                            color="white"
                        ),
                        ft.Image(
                            src=router.get_data("img_org"),
                            height = max_size_image,
                            width = max_size_image,
                        ),
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=half_box,
                alignment=ft.alignment.center_left
            )
    
    ao = ai_overlay(router=router, go_to=go_to)
    
    overlay_ai = ft.Container(
                        ao,
                        width=half_box,
                        alignment=ft.alignment.Alignment(-0.4, 0),
                        blur=ft.Blur(2,2,ft.BlurTileMode.MIRROR),
                    )
    
    content =ft.Row([
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
                    overlay_ai,
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
            )
    
    return content
