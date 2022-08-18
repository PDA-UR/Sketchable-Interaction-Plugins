import shutil

from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.FilesystemEntry import FilesystemEntry
from plugins.standard_environment_library._standard_behaviour_mixins.Transportable import Transportable
from plugins.standard_environment_library.filesystem import InteractionPriorization
import os


class File(Transportable, FilesystemEntry):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ File __"
    region_display_name = "File"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ File __", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)
        self.prio = None
        x, y = self.absolute_x_pos(), self.absolute_y_pos()
        self.create_region_via_class([[x, y], [x, y + 4], [x + 4, y + 4], [x + 4, y]], InteractionPriorization, {"parent": self})

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

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
                self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
                self.set_QML_data("height", self.height, PySI.DataType.INT)
                self.is_ready = True

                if self.parent is not None and self.path != "":
                    centerx, centery = self.parent.aabb[0].x + (self.parent.aabb[3].x - self.parent.aabb[0].x) / 2, self.parent.aabb[0].y + (self.parent.aabb[1].y - self.parent.aabb[0].y) / 2
                    self.prio.move(self.absolute_x_pos() - self.prio.absolute_x_pos(), self.absolute_y_pos() - self.prio.absolute_y_pos())
                    self.move(self.parent.x + centerx - self.aabb[0].x - self.width / 2, centery - self.aabb[0].y - self.height / 2 + self.parent.y)
        else:
            self.width = int(self.icon_width * 2)
            self.height = int(self.icon_height * 2)
            self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
            self.set_QML_data("height", self.height, PySI.DataType.INT)

        fname = self.get_QML_data("text", PySI.DataType.STRING)
        if self.is_new([fname], ["text"]):
            if fname != "":
                self.entryname = fname
                self.set_QML_data("name", fname, PySI.DataType.STRING)

                if self.parent is not None or self.path != "":
                    new_path = self.path[:self.path.rfind("/") + 1] + fname
                    os.rename(self.path, new_path)
                    self.path = new_path

        colls = [k for i, k in self.present_collisions()]

        if self.is_ready and self.was_moved() and "__ FolderIcon __" not in colls and "__ FolderBubble __" not in colls and self.path != self.root_path:
            new_path = self.desktop_path + "/" + self.entryname
            if self.path != new_path:
                shutil.move(self.path, new_path)
                self.path = new_path

                self.set_QML_data("name", self.entryname, PySI.DataType.STRING)

                if self.parent is not None:
                    if self in self.parent.linked_content:
                        self.parent.linked_content.remove(self)

                self.parent = None

    def remove(self):
        self.prio.delete()
        self.prio.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.prio._uuid, PySI.LinkingCapability.POSITION)
        super().remove()
