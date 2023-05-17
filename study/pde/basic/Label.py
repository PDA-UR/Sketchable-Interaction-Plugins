from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.study.pde.tools.Magnet import Magnet

from plugins.E import E


class Label(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Label __"
    region_display_name = "Label"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Label, self).__init__(shape, uuid, "", Label.regiontype, Label.regionname, kwargs)
        self.qml_path = self.set_QML_path("Label.qml")

        self.color = kwargs["color"]
        self.text = kwargs["text"]
        self.parent = kwargs["parent"]
        self.with_border = False
        self.shape_rec = "" if "shape_recognition" not in kwargs.keys() else kwargs["shape_recognition"]
        self.parent.tags.append(self)

        self.parent.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

        Magnet.registered_colors.append(self.color)

        if self.shape_rec != "":
            Magnet.registered_shapes.append(self.shape_rec)

        self.set_QML_data("width", float(self.width), PySI.DataType.FLOAT)
        self.set_QML_data("height", float(self.height), PySI.DataType.FLOAT)
        self.set_QML_data("text", self.text, PySI.DataType.STRING)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_enter("__ON_TAGGING_LABEL__", SIEffect.EMISSION)
    def on_tagging_enter_emit(self, other):
        return self

    @SIEffect.on_leave("__ON_TAGGING_LABEL__", SIEffect.EMISSION)
    def on_tagging_leave_emit(self, other):
        return self