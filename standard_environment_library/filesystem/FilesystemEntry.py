from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
import os, time

class FilesystemEntry(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FilesystemEntry __"
    region_display_name = "FilesystemEntry"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ FilesystemEntry __", kwargs: dict = {}) -> None:
        super(FilesystemEntry, self).__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)

        self.root_path = "/home/juergen/Desktop/test" if "root_path" not in kwargs else kwargs["root_path"]

        cw, ch = self.context_dimensions()
        self.path = "" if "path" not in kwargs.keys() else kwargs["path"]
        self.entryname = "" if self.path == "" else self.path[self.path.rfind("/") + 1:]
        self.parent = None if "parent" not in kwargs else kwargs["parent"]
        self.parent_level = -1 if "parent_level" not in kwargs.keys() else kwargs["parent_level"]
        self.evaluate_enveloped = True
        self.icon_width = cw // 39
        self.icon_height = ch // 17
        self.text_height = ch // 22
        self.color = PySI.Color(0, 0, 0, 0)
        self.default_color = PySI.Color(0, 0, 0, 0)
        self.border_color = PySI.Color(0, 0, 0, 0)
        self.text_color = "FF000000"
        self.__qml_data__ = {}
        self.is_ready = False
        self.with_border = False
        self.default_with_border = False
        if self.parent is not None and self.path != "":
            self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", self.entryname, PySI.DataType.STRING)
        self.parenting_time = 0

        if self.path != "":
            self.creation_time = time.ctime(os.path.getctime(self.path))
            self.modification_time = time.ctime(os.path.getmtime(self.path))

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        container_width = self.get_QML_data("container_width", PySI.DataType.FLOAT)
        container_height = self.get_QML_data("container_height", PySI.DataType.FLOAT)

        if container_width != 0 and container_height != 0:
            if self.is_new([container_width, container_height], ["container_width", "container_height"]):
                self.shape = PySI.PointVector(
                    [[self.aabb[0].x, self.aabb[0].y],
                     [self.aabb[0].x, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y]
                     ]
                )

                self.width = int(container_width)
                self.height = int(container_height)
                if self.parent is not None and self.path != "":
                    centerx, centery = self.parent.aabb[0].x + (self.parent.aabb[3].x - self.parent.aabb[0].x) / 2, self.parent.aabb[0].y + (self.parent.aabb[1].y - self.parent.aabb[0].y) / 2
                    self.move(self.parent.x + centerx - self.aabb[0].x - self.width / 2, centery - self.aabb[0].y - self.height / 2 + self.parent.y)
                self.is_ready = True

        fname = self.get_QML_data("text", PySI.DataType.STRING)
        if self.is_new([fname], ["text"]):
            if fname != "":
                self.entryname = fname
                self.set_QML_data("name", fname, PySI.DataType.STRING)

                if self.parent is not None or self.path != "":
                    new_path = self.path[:self.path.rfind("/") + 1] + fname
                    os.rename(self.path, new_path)
                    self.path = new_path

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

    @SIEffect.on_enter("__HIGHLIGHT_ADDITION__", SIEffect.RECEPTION)
    def on_highlight_addition_enter_recv(self):
        pass

    @SIEffect.on_continuous("__HIGHLIGHT_ADDITION__", SIEffect.RECEPTION)
    def on_highlight_addition_continuous_recv(self):
        pass

    @SIEffect.on_leave("__HIGHLIGHT_ADDITION__", SIEffect.RECEPTION)
    def on_highlight_addition_leave_recv(self):
        pass

    @SIEffect.on_continuous("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_continuous_recv(self):
        pass

    @SIEffect.on_continuous("ADD_TO_FOLDERICON", SIEffect.RECEPTION)
    def on_add_to_folder_continuous_recv(self):
        pass

    @SIEffect.on_enter("__FOLDER_SPLIT__", SIEffect.RECEPTION)
    def on_folder_split_enter_recv(self):
        pass

    def on_move_enter_recv(self, cursor_id, link_attrib):
        self.with_border = True
        super().on_move_enter_recv(cursor_id, link_attrib)

    def on_move_leave_recv(self, cursor_id, link_attrib):
        self.with_border = self.default_with_border
        super().on_move_leave_recv(cursor_id, link_attrib)

    def remove(self):
        self.delete()