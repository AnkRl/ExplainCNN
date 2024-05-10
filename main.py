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
    page.on_route_change = router.route_change
    router.page = page
    page.add(
        ft.Stack([
            ft.Image(src="assets/background.jpg"),
            router.body
        ])
    )

    page.go('/0')

ft.app(target=main, assets_dir="assets")