import flet as ft
from views.routes import router
from user_controls.app_bar import NavBar
import utils
import json

def main(page: ft.Page):

    # Set basic properties
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed = utils.IMAGE_ORANGE, color_scheme = ft.ColorScheme(primary=utils.IMAGE_ORANGE_DARK, secondary=utils.IMAGE_ORANGE_LIGHT, tertiary=utils.IMAGE_YELLOW))
    #ft.colors.SECONDARY = utils.IMAGE_ORANGE_60
    #color_scheme_seed = utils.IMAGE_ORANGE, 

    page.window_full_screen=True
    page.padding = 0

    # Load Translator
    with open("assets/de.json", "rb") as f:
        text = json.load(f)    
    router.set_data("translator", text)
    router.set_data("lng", "DE")

    # Add Appbar
    page.appbar = NavBar(page)
    
    def page_resize(e):
        utils.CENTER_X = page.width * 0.5
        utils.CENTER_Y = page.height * 0.5
        # page.snack_bar = ft.SnackBar(ft.Text(f'New page size => width: {page.width} ({utils.CENTER_X}), height: {page.height} ({utils.CENTER_Y})'))
        # page.snack_bar.open = True
        page.update()

    
    page.on_resize = page_resize
    page.on_route_change = router.route_change
    router.page = page
    
    utils.CENTER_X = page.width * 0.5
    utils.CENTER_Y = page.height * 0.5

    page.add(
        ft.Stack([
            ft.Image(src="assets/background.jpg"),
            router.body
        ])
    )

    page.go('/start')
    page.update()

ft.app(target=main, assets_dir="assets")