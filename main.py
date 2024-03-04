from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivymd.theming import ThemeManager


from components.screens import StartScreen, ModeScreen, CompareScreen
from image_manager import ImageManager
from utils import resource_path

from os import listdir, environ
environ["KIVY_NO_CONSOLELOG"] = "1"

kv_path = resource_path("./design/")
for file in listdir(kv_path): 
    Builder.load_file(kv_path+file) 

#Builder.load_file(resource_path("design_2.kv")) 


# App Class
class ExplainerApp(MDApp):
    def build(self):
        #Setting colors
        self.theme_cls.theme_style = "Light"
        self.theme_cls.theme_bg_color = "GreyBlue"
        self.theme_cls.primary_palette= "Cyan"
        self.theme_cls.backgroundColor = "Black"

        self.font_color = (0.13,0.13,0.13)
        self.button_size = "25sp"
        self.label_size = "20sp"

        # Instantiate image manager
        image_manager = ImageManager()

        #Need a ScreenManager to manage        
        sm = MDScreenManager()
        # sm.transition = SlideTransition()
        # sm.transition.direction = "up"
        sm.add_widget(StartScreen(image_manager=image_manager, name='start'))
        sm.add_widget(ModeScreen(image_manager=image_manager, name='mode'))
        sm.add_widget(CompareScreen(image_manager=image_manager, name='compare'))
        
        return sm

# Run App
ExplainerApp().run()