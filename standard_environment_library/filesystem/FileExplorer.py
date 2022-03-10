from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.filesystem.Folder import Folder
from plugins.standard_environment_library.filesystem.FolderIcon import FolderIcon
from plugins.E import E

import os


class FileExplorer(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ FileExplorer __"
    region_display_name = "FileExplorer"
    root_path = "/home/juergen/Desktop/test"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/file_manager.png", FileExplorer.regiontype, FileExplorer.regionname, kwargs)
        self.source = "libStdSI"
        self.path = FileExplorer.root_path
        self.color = PySI.Color(164, 216, 216, 255)
        self.qml_path = self.set_QML_path("FileExplorer.qml")

        if not os.path.exists(self.path + "/.temp"):
            os.mkdir(self.root_path + "/.temp")

        if "DRAWN" in kwargs.keys() and kwargs["DRAWN"]:
            if not self.path in [r.path for r in self.current_regions() if r.regionname == Folder.regionname or r.regionname == FolderIcon.regionname]:
                self.create_region_via_name(self.shape, Folder.regionname, False, {"parent": None, "path": self.path, "open": False, "hierarchy_level": 0, "root": True, "root_path": self.path})
            self.delete()

    # @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    # def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
    #     pass