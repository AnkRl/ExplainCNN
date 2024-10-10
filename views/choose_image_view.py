import flet as ft
import utils

def ChooseImageView(router):
    translator = router.get_data("translator")["choose_image_view"]
    width, height = utils.get_size(0.9,0.9)


    def handle_click(e: ft.ControlEvent):
        router.set_data("img_org", e.control.data)
        router.image_manager.set_image(e.control.data)
        flag = router.get_data("flag")
        dlg = ft.AlertDialog(content=
                                ft.Container(
                                        content=ft.Image(src="assets/loading.svg",
                                                    width=(width*0.9)/3),
                                        width= width,
                                        height= height,
                                        border_radius= 18,
                                        #border= ft.border.all(1, "#44f4f4f4"),
                                        alignment=ft.alignment.center,
                                        blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR)
                                    ),
                                modal = True,
                                bgcolor=ft.colors.with_opacity(0, ft.colors.PRIMARY)
                                )
        router.set_data("loading", dlg)
        dlg = router.get_data("loading")
        e.page.open(dlg)
        
        if flag == "EXPLAIN":
            e.page.go("/compare")
        else:
            e.page.go("/attack")
        

    def goto_camera(e: ft.ControlEvent):
        e.page.go("/camera")

    all_images = router.image_manager.image_list
    images = ft.GridView(
            expand=1,
            runs_count=3,
            max_extent=300,
            child_aspect_ratio=1.0,
            spacing=1,
            run_spacing=1,
            width=width*0.6
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
    images.controls.append(
        ft.Container(
                        image_src="assets/camera.png",
                        margin=10,
                        padding=10,
                        alignment=ft.alignment.center,
                        width=500,
                        height=500,
                        border_radius=5,
                        ink=True,
                        data= None,
                        on_click= lambda e: goto_camera(e)
                    )
    )

    image = ft.Image(
        src = "assets/gallery_icon.svg",
        width=width*0.1,
    )
    title = ft.Text(
        translator["title"],
        color= "white",
        theme_style=ft.TextThemeStyle.HEADLINE_SMALL
    )
    title_bar = ft.Row([
                    image,
                    title
                ],
                width=width*0.6
                )

    content = ft.Column([
                        title_bar,
                        images
                    ],
                    # Params for content column
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20
                    
                    )
    return content

