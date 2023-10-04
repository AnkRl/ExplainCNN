from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.widget import MDWidget
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, Line
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.image import Image
from kivymd.uix.label import MDLabel
from kivy.lang import Builder

import os
import random
from copy import deepcopy
Builder.load_file("designMD.kv")

# Welcoming screen, for starting the game
class StartScreen(MDScreen):
    pass
###

class MainScreen(MDScreen):
    buttons = {
            'Foto aufnehmen': [
                'camera-plus-outline',
                "on_press", lambda x: print("Foto aufnehmen")
            ],
            'Zufallsbild': [
                'image-multiple-outline',
                "on_press", lambda x: print("Zufallsbild")
            ],
        }
    image_path = StringProperty()

    def compare(self):
        print("Vergleichen")

# App Class
class ExplainerApp(MDApp):
    def build(self):
        #Setting colors
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Cyan"

        #Need a ScreenManager to manage        
        sm = MDScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainScreen(name='main'))

        return sm

# Run App
ExplainerApp().run()