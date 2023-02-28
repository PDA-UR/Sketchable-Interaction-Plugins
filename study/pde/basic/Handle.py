from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class Handle(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Handle __"
    region_display_name = "Handle"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Handle, self).__init__(shape, uuid, "res/resize.png", Handle.regiontype, Handle.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.qml_path = self.set_QML_path("Handle.qml")
        self.color = PySI.Color(128, 128, 128, 128)
        self.border_width = int(1 * cw / 1920)

        self.parent = kwargs["parent"]
        self.corner = kwargs["corner"]
        self.num = kwargs["num"]

        self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.create_link(self._uuid, "__RESIZE__", self.parent._uuid, "__RESIZE__")
        self.parent.handles.append(self)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y, kwargs={}):
        self.move(self.x + rel_x, self.y + rel_y)

        self.delta_x, self.delta_y = rel_x, rel_y
        self.transform_x += int(self.delta_x)
        self.transform_y += int(self.delta_y)

        if self.is_under_user_control:
            self.mouse_x = abs_x
            self.mouse_y = abs_y
        else:
            self.mouse_x = 0
            self.mouse_y = 0

        if "moved_by_target" not in kwargs.keys():
            self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, self.resize())

    @SIEffect.on_link(SIEffect.EMISSION, "__RESIZE__")
    def resize(self):
        return self.num, {}

