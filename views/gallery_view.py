import flet as ft
import utils

def GalleryView(router):
    width, height= utils.get_size_main_container()

    def handle_click(e: ft.ControlEvent):
        router.set_data("img_org", e.control.data)
        router.image_manager.set_image(e.control.data)
        e.page.go("/compare")#, data=text_field.value)

    all_images = router.image_manager.image_list
    images = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=1,
            run_spacing=1,
            width=width*0.8
        )
    images.controls = [
                    ft.Container(
                        image_src=img,
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        width=500,
                        height=500,
                        border_radius=5,
                        ink=True,
                        data= img,
                        on_click= lambda e: handle_click(e)
                    )
                    for img in all_images]

    return images
