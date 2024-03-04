from kivymd.uix.screen import Screen as MDScreen
from kivy.uix.image import Image, CoreImage
from kivymd.theming import ThemableBehavior

from .cards import ModeOptionCard, KIOverlayCard
from .popup import CameraPopup, GalleryPopup
from .widget import DrawingWidget, KIOverlayWidget, UserAnnotationsWidget



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
        super().__init__(**kw)
    
    def get_properties(self):
        # Adding the drawing area
        self.ids.compare_box.add_widget(
            DrawingWidget(self.image_manager.original_image),
        )
        # Adding ki overlay
        # Bind event to hit_compare somehow... 
        ki_overlay = KIOverlayCard()
        ki_overlay.bind(hit_compare=self.trigger_show_ki_image)
        self.ids.compare_box.add_widget(ki_overlay)
        
    def trigger_show_ki_image(self, value,_):
        # TODO less hacky here
        self.ids.compare_box.remove_widget(self.ids.compare_box.children[0])
        self.show_ki_image()
            

    def set_properties(self):
        #Clean up
        images = [i for i in self.ids.compare_box.children]
        for i in images:
            self.ids.compare_box.remove_widget(i)

    def show_ki_image(self):
        self.ids.compare_box.add_widget(
            self._img2kivy(self.image_manager.ki_image) 
        )

    def _img2kivy(self, image):
        import io
        image_bytes = io.BytesIO()
        image.save(image_bytes, format="png")
        image_bytes.seek(0)

        img = CoreImage(image_bytes, ext="png").texture

        new_img = Image()
        new_img.texture = img
        image_bytes.close()
        
        return new_img
    

