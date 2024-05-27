from typing import Callable
import flet as ft
from image_manager import ImageManager
from utils import get_size_with_margin

class Router:
    def __init__(self):
        self.data = dict()
        self.routes = {}
        self.body = ft.Container()
        self.image_manager = ImageManager()

    def set_route(self, stub: str, view: Callable):
        self.routes[stub] = view
    
    def set_routes(self, route_dictionary: dict):
        """Sets multiple routes at once. Ex: {"/": IndexView }"""
        self.routes.update(route_dictionary)

    def route_change(self, route):
        _page = route.route.split("?")[0]
        queries = route.route.split("?")[1:]

        for item in queries:
            key = item.split("=")[0]
            value = item.split("=")[1]
            self.data[key] = value.replace('+', ' ')
        
        width, height, vertical, horizontal = get_size_with_margin(0.8,0.8)

        self.body.content = ft.Container(
                                ft.Container(
                                    content = self.routes[_page](self),
                                    # Params for Main content container
                                    width= width,
                                    height= height,
                                    border_radius= 18,
                                    #border= ft.border.all(1, "#44f4f4f4"),
                                    alignment=ft.alignment.center,
                                    blur= ft.Blur(10,12,ft.BlurTileMode.MIRROR)
                                ),
                                margin= ft.margin.symmetric(horizontal=horizontal, vertical=vertical),
                                alignment=ft.alignment.center,
                            )
        self.body.update()

    def set_data(self, key, value):
        self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)

    def get_query(self, key):
        return self.data.get(key)

