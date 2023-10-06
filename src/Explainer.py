import logging
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line
from kivy.properties import StringProperty
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.lang import Builder

from network.efficient_net import EfficientNet

import os
import random
import numpy as np

Builder.load_file("design.kv") 
logging.getLogger('matplotlib.font_manager').disabled = True

# Welcoming screen, for starting the game
class WelcomeScreen(Screen):
    def load_model(self):        
        self.KI = EfficientNet()        

    # Some clean up
    if os.path.exists("user_image.png"): os.remove("user_image.png")
    if os.path.exists("ki_image.png"): os.remove("ki_image.png")
    if os.path.exists("original_image.png"): os.remove("original_image.png")


###

# Choose whether to use a random image or take a picture
class ChoiceScreen(Screen):
    image_path = StringProperty()

    def get_properties(self):
        self.KI = self.manager.get_screen('welcome').KI
        self.image_path= "images/" + random.choice([x for x in os.listdir("images")])

    def save_properties(self):
        self.KI.pass_image_to_net(self.image_path)
    
    def open_camera(self):
        popup = CameraPopup()
        popup.open()
        self.image_path = "picture.png"

class CameraPopup(Popup):
    def capture(self):
        camera = self.ids['camera']
        if os.path.exists("picture.png"):
            os.remove("picture.png")
        camera.export_to_png("picture.png")
        
###

# Classify the image and mark the part where you recognized it
class MarkScreen(Screen):
    text_user = StringProperty()
    image_user = StringProperty("user_image.png")
    image_path = StringProperty()
    
    # on_enter: we wanna have the image path, declared in choice screen
    def get_properties(self):
        self.KI = self.manager.get_screen('choice').KI
        self.image_path = self.manager.get_screen('choice').image_path

    #TODO: Get user input for text value
    def get_text(self):
        self.text_user = self.ids.textbox.text
    
    #TODO: Wrapper for exit Screen (i.e. triggered when clicking the Compare AI Button)
    def save_properties(self):
        self.get_text()
        self.image_user = self.ids.drawing.save()
        self.ids.drawing.clean()
    

class DrawingWidget(Widget):
    def save(self):
        self.export_to_png("user_image.png")
        return "user_image.png"

    def clean(self):
        rectangle = self.canvas.children[:2]
        self.canvas.clear()
        # TODO: Less hacky solution please...
        self.canvas.children = rectangle
        

    def out_of_boundary(self, touch):
        size_x, size_y = self.size
        pos_x, pos_y = self.pos
        x = touch.pos[0]
        y = touch.pos[1]
        
        if x > pos_x and x < size_x + pos_x and y > pos_y and y < size_y + pos_y:
            return False
        else:
            return True

    # paint
    def on_touch_down(self, touch):        
        if self.out_of_boundary(touch):
            pass
        else:
            with self.canvas:
                Color(0, 0, 1, 0.7)
                self.line = Line(points=[touch.pos[0], touch.pos[1]], width=5)

    # paint
    def on_touch_move(self, touch):
        if self.out_of_boundary(touch):
            pass
        else:
            self.line.points = self.line.points + [touch.pos[0], touch.pos[1]]
    
###

# Compare your results with the AI (EfficientNet)
class ComparisonScreen(Screen):
    
    # on_enter: we wanna have the image path, declared in choice screen
    def get_values(self):
        self.KI = self.manager.get_screen('mark').KI
        self.text_user = self.manager.get_screen('mark').text_user
        self.text_ki = self.KI.prediction
        self.image_user = self.manager.get_screen('mark').image_user
        self.image_ki = self.KI.ki_image_path

        # Draw Image and set Title
        self.img_user = Image(source=self.image_user, nocache=True)
        self.ids.user.clear_widgets()
        self.ids.user.add_widget(Label(text=self.text_user, font_size="20sp", color= (0.13,0.13,0.13), size_hint=(1,0.3)))
        self.ids.user.add_widget(self.img_user)
        self.ids.ki.clear_widgets()
        self.img_ki = Image(source=self.image_ki, nocache=True)
        self.ids.ki.add_widget(Label(text=self.text_ki, font_size="20sp", color= (0.13,0.13,0.13), size_hint=(1,0.3)))
        self.ids.ki.add_widget(self.img_ki)

###

# App Class
class ExplainerApp(MDApp):
    def build(self):
        #Setting colors
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.accent_palette = "Cyan"

        self.font_color = (0.13,0.13,0.13)
        self.button_size = "25sp"
        self.label_size = "20sp"

        #Need a ScreenManager to manage        
        sm = ScreenManager()
        sm.transition = SlideTransition()
        sm.transition.direction = "up"
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(ChoiceScreen(name='choice'))
        sm.add_widget(MarkScreen(name='mark'))
        sm.add_widget(ComparisonScreen(name='comparison'))
        
        return sm

# Run App
ExplainerApp().run()