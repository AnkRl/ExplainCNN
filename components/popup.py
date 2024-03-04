from kivy.uix.popup import Popup

from .cards import GalleryImageCard

class GalleryPopup(Popup):
    '''
    Popup for choosing image from Gallery
    '''
    def __init__(self, image_manager, **kw):
        super().__init__(**kw)
        self.image_manager = image_manager        
        # Add images to grid
        for i in image_manager.image_list:
            self.ids.grid.add_widget(
                GalleryImageCard(image_path= i,
                           )
            )
        print(self.children)
    def on_click_image(self, image_path):
        self.image_manager.set_image(image_path)
        self.dismiss()

class CameraPopup(Popup):
    '''
    Popup for making a picture
    '''
    def __init__(self, **kw):
        super().__init__(**kw)
