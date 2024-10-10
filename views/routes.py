from views.Router import Router
from views.start_view import StartView
from views.compare_view import CompareView
from views.result_view import ResultView
from views.camera_view import CameraView
from views.language_view import LanguageView
from views.choose_image_view import ChooseImageView
from views.attack_view import AttackView

router = Router()

router.routes = {
  "/0": StartView,
  "/1": LanguageView,
  "/start": StartView,
  "/choose_image": ChooseImageView,
  "/compare": CompareView,
  "/result": ResultView,
  "/camera": CameraView,
  "/attack": AttackView
}