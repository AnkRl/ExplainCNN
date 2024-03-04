from kivy.properties import StringProperty
from kivy.properties import BooleanProperty

from kivymd.uix.card import MDCard

class ModeOptionCard(MDCard):
    ''' Class that handles the mode options (random, gallery, camera) '''
    icon = StringProperty()
    description = StringProperty()
    text = StringProperty()


class GalleryImageCard(MDCard):
    image_path = StringProperty()

class KIOverlayCard(MDCard):
    hit_compare = BooleanProperty(False)
