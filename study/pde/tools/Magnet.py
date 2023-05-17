from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.study.pde.basic.Combinator import Combinator
from plugins.study.pde.basic.Repository import Repository
from plugins.E import E


class Magnet(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Magnet __"
    region_display_name = "Magnet"
    registered_colors = []
    registered_shapes = []

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "res/magnet.png", Magnet.regiontype, Magnet.regionname, kwargs)
        self.qml_path = self.set_QML_path("Magnet.qml")
        self.color = PySI.Color(255, 0, 0, 255)

        x, y, w, h = self.aabb[0].x, self.aabb[0].y, 300, 300
        self.shape = PySI.PointVector([[x, y], [x, y + h], [x + w, y + h], [x + w, y]])

        self.set_QML_data("width", w, PySI.DataType.FLOAT)
        self.set_QML_data("height", h, PySI.DataType.FLOAT)

        self.repository = None
        self.combinator = None
        self.choices = []

        if "DRAWN" in kwargs and kwargs["DRAWN"]:
            self.create_region_via_name([[x + w / 2, y], [x + w / 2, y + h], [x + w, y + h], [x + w, y]], Repository.regionname, False, {"parent": self})
            self.create_region_via_name([[x, y], [x, y + h], [x + w / 2, y + h], [x + w / 2, y]], Combinator.regionname, False, {"parent": self})

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_enter("__ MAGNET_PULL __", SIEffect.EMISSION)
    def on_magnet_pull_enter_emit(self, other):
        color_filter = self.combinator.color_filter
        shape_filter = self.combinator.shape_filter

        return color_filter, shape_filter

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y
        return x, y, self.x, self.y, {"moved_by_target": True}

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        if not self.is_under_user_control:
            if self.repository is not None:
                self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.repository._uuid, PySI.LinkingCapability.POSITION)
                self.repository.on_deletion_enter_recv()
            if self.combinator is not None:
                self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.combinator._uuid, PySI.LinkingCapability.POSITION)
                self.combinator.on_deletion_enter_recv()

            for c in self.choices:
                c.delete()

            super().on_deletion_enter_recv()