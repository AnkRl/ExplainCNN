from kivymd.uix.screen import Screen as MDScreen
from kivy.properties import BooleanProperty
from kivymd.theming import ThemableBehavior

from .cards import ModeOptionCard
from .popup import CameraPopup, GalleryPopup
from .widget import KIOverlayWidget, UserAnnotationsWidget, KIImageWidget, UserImageWidget

from os import remove
from PIL import Image


class DefaultScreen(MDScreen, ThemableBehavior):
    '''
    Super Screen Class
    '''
    def __init__(self, image_manager, **kw):
        super().__init__(**kw)
        self.image_manager = image_manager

    def get_properties(self):
        pass
        #raise NotImplementedError("get_properties not implemented!")
    
    def set_properties(self):
        pass
        #raise NotImplementedError("set_properties not implemented!")

class StartScreen(DefaultScreen):
    '''
    Very first Screen to begin with. Loads everything in the background.
    '''
    # def __init__(self, image_manager, **kw):
    #     super().__init__(**kw)
        
    #     self.image_manager = image_manager


class ModeScreen(DefaultScreen):
    '''
    Class that handles the image choice. Can lead to 
        a gallery pop up, 
        a camera pop-up or 
        just continues with a random image
    Must inform CompareScreen 
        which mode it is in
        which image to choose
    '''
    def __init__(self, **kw):
        super().__init__(**kw)
        # Load the Mode Options
        self.ids.box.add_widget(
                ModeOptionCard(icon="image-outline",
                           description="In diesem Modus werden dir zufällig Bilder angezeigt, die du dann identifizieren kannst",
                           text="Zufall"
                           )
            )
        self.ids.box.add_widget(
                ModeOptionCard(icon="image-multiple-outline",
                           description="In diesem Modus kannst du dir ein Bild aussuchen, das du dann identifizieren kannst",
                           text="Galerie"
                           )
            )
        self.ids.box.add_widget(
                ModeOptionCard(icon="camera",
                           description="In diesem Modus kannst du ein Bild machen, das du dann identifizieren kannst",
                           text="Schnappschuss"
                           )
            )
    
    def on_click_option(self, option: str):
        if option == "Zufall":
            self.image_manager.random_image()
            self.manager.current = "compare"

        elif option == "Galerie":
            popup = GalleryPopup(self.image_manager)
            def next_screen(instance):
                self.manager.current = "compare"
            popup.bind(on_dismiss=next_screen)
            popup.open()
        
        else:
            popup = CameraPopup()
            def next_screen(instance):
                self.manager.current = "compare"
            popup.bind(on_dismiss=next_screen)
            popup.open()
    

class CompareScreen(DefaultScreen):
    '''
    Class that handles 
        the user annotations
        the comparison with the AI

    '''
    def __init__(self, **kw):
        self.network_status = BooleanProperty(True)
        super().__init__(**kw)
        # Get Boxlayout
        self.compare_box = self.ids.compare_box        

        # Set three main children (added dynamically and therefore not in .kv)
        self.ki_overlay = None
        self.user_annotations = None
        self.ki_image = None
    
    def get_properties(self):
        # If this function is triggered, images are chosen and can be set
        self.set_images()
        
        self.compare_box.add_widget(self.user_annotations)
        self.compare_box.add_widget(self.ki_overlay)
        
    def trigger_show_ki_image(self, value,_):
        # Remove Overlay 
        self.compare_box.remove_widget(self.ki_overlay)
        
        # Get user annotations and remove user annotation widget
        user_input = self.user_annotations.ids.userInput.text
        # save annotations
        self.user_annotations.ids.userAnnotations.children[0].export_to_png("temp.png", fmt="png")
        user_image = Image.open("temp.png")
        self.compare_box.remove_widget(self.user_annotations)

        # Add user and ki image
        self.compare_box.add_widget(UserImageWidget(user_input=user_input, user_image=user_image))
        self.compare_box.add_widget(self.ki_image)

    def set_properties(self):
        #Clean up
        images = [i for i in self.ids.compare_box.children]
        for i in images:
            self.ids.compare_box.remove_widget(i)
    
    def set_images(self):
        self.ki_overlay = KIOverlayWidget()
        self.ki_overlay.bind(hit_compare=self.trigger_show_ki_image)
        self.user_annotations = UserAnnotationsWidget(self.image_manager.original_image)         
    
    def get_ki_images(self):
        self.ki_overlay.network_status = self.image_manager.get_prediction()
        self.ki_image = KIImageWidget(self.image_manager.ki_image, self.image_manager.prediction)