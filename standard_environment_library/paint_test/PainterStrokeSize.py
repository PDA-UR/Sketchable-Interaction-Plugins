from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.paint_test.stroke_size_selection.PainterStrokeSizeSelectionSlider import PainterStrokeSizeSelectionSlider
from plugins.E import E


class PainterStrokeSize(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ PainterStrokeSize __"
    region_display_name = "PainterStrokeSize"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(PainterStrokeSize, self).__init__(shape, uuid, "res/stroke.png", PainterStrokeSize.regiontype, PainterStrokeSize.regionname, kwargs)
        self.qml_path = self.set_QML_path("PainterStrokeSize")
        self.color = PySI.Color(230, 230, 230, 255)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass
        x, y = self.relative_x_pos(), self.relative_y_pos() + self.height + 20
        slider_shape = [[x, y], [x, y + 30], [x + 300, y + 30], [x + 300, y]]

        self.create_region_via_name(slider_shape, PainterStrokeSizeSelectionSlider.regionname, False)
        self.delete()