import flet as ft
from views.routes import router
from user_controls.app_bar import NavBar
import utils
import json

def main(page: ft.Page):

    # Set basic properties
    page.theme_mode = "light"
    page.theme = ft.Theme(color_scheme_seed = utils.GREY_DARK, color_scheme = ft.ColorScheme(primary=utils.GREY_DARK, secondary=utils.GREY_LIGHT, tertiary=utils.IMAGE_YELLOW))
    #page.window.full_screen = True
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
        page.update()

    
    page.on_resized = page_resize
    page.on_route_change = router.route_change
    router.page = page
    
    page.bgcolor = ft.colors.TRANSPARENT
    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="assets/background.jpg",
            fit=ft.ImageFit.COVER,
            opacity=1,
        ),
    )
    utils.CENTER_X = page.width * 0.5
    utils.CENTER_Y = page.height * 0.5

    page.add(
        router.body
    )

    page.go('/start')
    page.update()

ft.app(target=main, assets_dir="assets")