from views.Router import Router
from views.start_view import StartView
from views.mode_view import ModeView
from views.compare_view import CompareView
from views.gallery_view import GalleryView
from views.result_view import ResultView
from views.camera_view import CameraView
from views.language_view import LanguageView

router = Router()

router.routes = {
  "/0": StartView,
  "/1": ModeView,
  "/2": LanguageView,
  "/gallery": GalleryView,
  "/start": StartView,
  "/mode": ModeView,
  "/compare": CompareView,
  "/result": ResultView,
  "/camera": CameraView
}