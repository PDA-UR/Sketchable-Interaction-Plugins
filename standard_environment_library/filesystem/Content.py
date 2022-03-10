from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.E import E
import os


class Content(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Content __"
    region_display_name = "Content"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ Content __", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)
        self.icon_width = 65
        self.icon_height = 75
        self.color = PySI.Color(0, 0, 0, 0)
        self.default_color = PySI.Color(0, 0, 0, 0)
        self.text_color = "FF000000"
        self.__qml_data__ = {}
        self.with_border = False
        self.is_initial = "initial" in kwargs and kwargs["initial"]
        self.parent = None if "parent" not in kwargs else kwargs["parent"]
        self.root_path = "/home/juergen/Desktop/test" if "root_path" not in kwargs else kwargs["root_path"]
        self.evaluate_enveloped = True
        self.is_ready = False
        self.parent_level = -1 if "hierarchy_level" not in kwargs.keys() else kwargs["hierarchy_level"]
        self.path = "" if "path" not in kwargs.keys() else kwargs["path"]
        self.is_removed = False

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        container_width = self.get_QML_data("container_width", PySI.DataType.FLOAT)
        container_height = self.get_QML_data("container_height", PySI.DataType.FLOAT)

        if container_width != 0 and container_height != 0:
            if self.is_new([container_width, container_height], ["container_width", "container_height"]):
                prev_x, prev_y = self.absolute_x_pos(), self.absolute_y_pos()
                self.shape = PySI.PointVector(
                    [[self.aabb[0].x, self.aabb[0].y],
                     [self.aabb[0].x, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y]
                     ]
                )

                self.width = int(container_width)
                self.height = int(container_height)
                self.is_ready = True
                if self.parent is not None:
                    self.move(self.parent.x + self.x, self.parent.y + self.y)
                    print("HERE0")
                    print(f"{prev_x, prev_y} to {self.absolute_x_pos(), self.absolute_y_pos()}")
                else:
                    print("HERE1")
                    print(f"{prev_x, prev_y} to {self.absolute_x_pos(), self.absolute_y_pos()}")
                print("----")

    def is_new(self, values, keys):
        is_new = False

        for v, k in zip(values, keys):
            if k not in self.__qml_data__:
                is_new = True
            else:
                if k in self.__qml_data__ and self.__qml_data__[k] != v:
                    is_new = True

            self.__qml_data__[k] = v

        return is_new

    def rename(self):
        fname = self.get_QML_data("text", PySI.DataType.STRING)
        if self.path == self.root_path:
            self.set_QML_data("name", self.path, PySI.DataType.STRING)
        else:
            if self.is_new([fname], ["text"]):
                if fname != "":
                    fname = fname.replace("-", "").replace("\n", "")
                    fname = fname[fname.rfind("/") + 1:]
                    original_path = self.path
                    self.path = self.path[:self.path.rfind("/")] + "/" + fname
                    self.set_QML_data("name", fname, PySI.DataType.STRING)
                    os.rename(original_path, self.path)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass

    @SIEffect.on_continuous("__PARENT_CONTENT_ICON__", SIEffect.RECEPTION)
    def on_content_icon_continuous_recv(self):
        pass

    @SIEffect.on_leave("__PARENT_CONTENT_ICON__", SIEffect.RECEPTION)
    def on_content_icon_leave_recv(self):
        pass

    @SIEffect.on_continuous("__PARENT_CONTENT__", SIEffect.RECEPTION)
    def on_content_continuous_recv(self):
        pass

    @SIEffect.on_enter("__HIDE_ENTRY_", SIEffect.RECEPTION)
    def on_hide_entry_enter_recv(self):
        self.delete()

    @SIEffect.on_enter("__PARENT_CONTENT__", SIEffect.RECEPTION)
    def on_content_enter_recv(self) -> None:
        if self.is_under_user_control:
            self.set_QML_data("name", self.filename if hasattr(self, "filename") else self.foldername, PySI.DataType.STRING)

    @SIEffect.on_leave("__PARENT_CONTENT__", SIEffect.RECEPTION)
    def on_content_leave_recv(self) -> None:
        if self.is_under_user_control:
            self.set_QML_data("name", self.path, PySI.DataType.STRING)
