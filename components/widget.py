from kivy.graphics import Color, Line
from kivy.uix.image import Image, CoreImage
from kivy.properties import BooleanProperty
from  kivy.uix.boxlayout import BoxLayout

from io import BytesIO
from utils import img2kivy

class KIOverlayWidget(BoxLayout):
    hit_compare = BooleanProperty(False)

class UserImageWidget(BoxLayout):
    def __init__(self, user_input, user_image, **kwargs):
        self.user_prediction = user_input
        super().__init__(**kwargs)
        self.ids.userImage.add_widget(img2kivy(image=user_image))

class KIImageWidget(BoxLayout):
    def __init__(self, image=None, prediction="", **kwargs):
        self.prediction = prediction
        super().__init__(**kwargs)        
        self.ids.kiImage.add_widget(img2kivy(image=image))

class DrawingWidget(Image):
    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)
        
        image_bytes = BytesIO()
        image.save(image_bytes, format="png")
        image_bytes.seek(0)

        img = CoreImage(image_bytes, ext="png").texture
        self.texture = img

        image_bytes.close()
        self.line = Line()

    def out_of_boundary(self, touch):
        size_x, size_y = self.width, self.height
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

class UserAnnotationsWidget(BoxLayout):
    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)
        self.ids.userAnnotations.add_widget(DrawingWidget(image))
