import flet as ft
from views.routes import router
from user_controls.app_bar import NavBar
import utils

def main(page: ft.Page):

    page.theme_mode = "light"
    page.theme = ft.theme.Theme(color_scheme_seed = utils.IMAGE_ORANGE)
    #page.window_full_screen=True
    page.padding = 0
    page.appbar = NavBar(page)
    
    utils.CENTER_X = page.width * 0.5
    utils.CENTER_Y = page.height * 0.5
    
    def page_resize(e):
        utils.CENTER_X = page.width * 0.5
        utils.CENTER_Y = page.height * 0.5
        # page.snack_bar = ft.SnackBar(ft.Text(f'New page size => width: {page.width} ({utils.CENTER_X}), height: {page.height} ({utils.CENTER_Y})'))
        # page.snack_bar.open = True
        page.update()

    page.on_resize = page_resize
    page.on_route_change = router.route_change
    router.page = page
    page.add(
        ft.Stack([
            ft.Image(src="assets/background.jpg"),
            router.body
        ])
    )

    page.go('/start')

ft.app(target=main, assets_dir="assets")