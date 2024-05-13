import flet as ft

# handling translations
import utils 
translator = utils.translator["mode_view"]

import os

def GalleryView(router):
    
    def go_to(e: ft.ControlEvent):
        e.page.go("/compare")
    
    def handle_click(e: ft.ControlEvent):
        router.set_data("img_org", e.control.data)
        router.image_manager.set_image(e.control.data)
        e.page.go("/compare")#, data=text_field.value)

    all_images = router.image_manager.image_list
    images = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=1,
            run_spacing=1,
        )
    images.controls = [
                    ft.Container(
                        image_src=img,
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        width=150,
                        height=150,
                        border_radius=10,
                        ink=True,
                        data= img,
                        on_click= lambda e: handle_click(e)
                    )
                    for img in all_images]

    return images