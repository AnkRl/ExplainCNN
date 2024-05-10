from views.Router import Router, DataStrategyEnum
from views.start_view import StartView
from views.mode_view import ModeView
from views.compare_view import CompareView

router = Router(DataStrategyEnum.ROUTER_DATA)

router.routes = {
  "/0": StartView,
  "/1": ModeView,
  "/2": CompareView,
}