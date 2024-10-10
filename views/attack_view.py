
import flet as ft
import flet.canvas as cv
import utils
from assets.categories import *

class State:
    x: float
    y: float
state = State()

def AttackView(router):
    dlg = router.get_data("loading")
    translator = router.get_data("translator")["compare_view"]
    router.image_manager.get_attack()

    curr_lng = router.get_data("lng")
    categories = de_categories() if curr_lng is "DE" else en_categories()
    
    dlg.open = False
    router.page.update()

    # Calculate widths
    width, height = utils.get_size_main_container()    
    max_size_image = width/3
    half_box = width*0.5
    button_size = 100
    size_user = width*0.15
    size_ai = width*0.14
    
    def goto(e):
        e.page.go("/start")
    
    def dummy(e):
        pass

    def get_chips(labels): 
        chips = []
        chips.append(
            ft.Chip(
                    label=ft.Text(labels[-1]),
                    bgcolor=utils.IMAGE_YELLOW,
                    autofocus=True,
                    selected= True,
                    on_select=dummy
                )
        )
        for a in labels[:2]:
            chips.append(
                ft.Chip(
                    label=ft.Text(a),
                    bgcolor=utils.IMAGE_YELLOW,
                    autofocus=True,
                    selected= False,
                    on_select=dummy,
                )
            )
        return chips
    
    def get_labels(pred):
        labels = []
        idx = pred[0]
        probs = pred[1]
        for i in range(3):
            guess = categories[idx[i]]
            prob = round(probs[i],1)
            labels.append(f"{guess} ({prob}%)")
        return get_chips(labels)

    repeat_button = ft.GestureDetector(
        ft.Image(
            src="assets/gallery_icon.svg",
            width=width*0.1,
        ),
        on_tap=goto,
         bottom = 0, left = width*0.45
    )

    image_keys = {
        "clean" : 0,
        "pixel" : 1,
        "adversarial": 2,
        "xai_clean": 3,
        "xai_adversarial":4
    }

    image_list = [
            router.image_manager.image_b64,
            router.image_manager.attack_image,
            router.image_manager.composed_attack_image,
            router.image_manager.ki_image,
            router.image_manager.ki_image_adv,
    ]

    label_list = [
            get_labels((router.image_manager.prediction, router.image_manager.probs)),
            get_labels(router.image_manager.pred_pxl),
            get_labels(router.image_manager.pred_adv),
            get_labels((router.image_manager.prediction, router.image_manager.probs)),
            get_labels(router.image_manager.pred_adv)
    ]

    columns = [ft.Column([
                    ft.Row(label_list[i], width= max_size_image),
                    ft.Image(
                        src_base64= image_list[i],
                        width = max_size_image,
                        height = max_size_image,
                    )
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                )
        for i in range(5)
    ]

    switchers = {
        "clean": ft.AnimatedSwitcher(
                    content=columns[image_keys["clean"]],
                    duration=100,
                    reverse_duration=100),
        "adversarial": ft.AnimatedSwitcher(
                    content=columns[image_keys["adversarial"]],
                    duration=100,
                    reverse_duration=100),
            }
   
    def show(e, switcher, col_default, col_change):  
        if switchers[switcher].content == columns[image_keys[col_default]]:
            switchers[switcher].content = columns[image_keys[col_change]]
            e.control.selected = False
        else:
            switchers[switcher].content = columns[image_keys[col_default]]
            e.control.selected = True

        e.control.update()
        switchers[switcher].update()
    
    button_attack = ft.IconButton(
            icon=ft.icons.SEARCH_ROUNDED,
            selected_icon=ft.icons.SEARCH_OFF_ROUNDED,
            on_click=lambda e: show(e,"clean", "pixel", "clean"),
            selected=False,
            style=ft.ButtonStyle(color={"selected": ft.colors.PRIMARY, "": ft.colors.SECONDARY}),
            icon_size= button_size*0.4,
            bottom =  height*0.08, 
            left = width * 0.17
        )
    button_xai_c = ft.IconButton(
                icon=ft.icons.AUTO_FIX_HIGH,
                selected_icon=ft.icons.AUTO_FIX_OFF,
                on_click=lambda e: show(e, "clean", "xai_clean", "clean"),
                style=ft.ButtonStyle(color={"selected": ft.colors.PRIMARY, "": ft.colors.SECONDARY}),
                icon_size= button_size*0.4,
                bottom =  height*0.08, 
                left = width*0.22
            )
    button_xai_a = ft.IconButton(
                icon=ft.icons.AUTO_FIX_HIGH,
                selected_icon=ft.icons.AUTO_FIX_OFF,
                on_click=lambda e: show(e, "adversarial", "xai_adversarial", "adversarial"),
                style=ft.ButtonStyle(color={"selected": ft.colors.PRIMARY, "": ft.colors.SECONDARY}),
                icon_size= button_size*0.4,
                bottom = height*0.08, 
                left = width * 0.52
            )

    repeat_button = ft.IconButton(
            	    icon = ft.icons.CACHED_ROUNDED, 
                    icon_size= button_size*0.7,
                    on_click=goto,
                    style=ft.ButtonStyle(color={"": ft.colors.SECONDARY}),
                    bottom = 0, 
                    left = width*0.47)

    row_right = ft.Container(
                ft.Column([
                    switchers["adversarial"],
                    # ft.Row([
                    #     button_dummy,
                    #     button_xai_a
                    # ],
                    # alignment=ft.alignment.center)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=half_box,
                alignment=ft.alignment.center_left
            )
    
    row_left =  ft.Container(
                ft.Column([
                    switchers["clean"]
                    # ft.Row([
                    #     button_attack,
                    #     button_xai_c
                    # ],
                    # alignment=ft.alignment.center)
                ],
                # Params for content column
                alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=half_box,
                alignment=ft.alignment.center_right
            )
    content = ft.Stack([
                ft.Image(
                    src = "assets/ai2.svg",
                    width = size_user,
                    top=0,
                    left = 10),
                ft.Image(
                        src = "assets/attack.svg",
                        width = size_ai,
                        top=0,
                        right=10),
                ft.Row([
                    row_left,
                    row_right
                ],
                # Params for content row
                width=width,
                height=height,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                repeat_button,
                button_attack,
                button_xai_a,
                button_xai_c                
            ],
            )
    return content