from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.filesystem.FolderBubble import FolderBubble
from plugins.standard_environment_library.filesystem.FolderIcon import FolderIcon
from plugins.E import E


class FilesystemAccess(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ FilesystemAccess __"
    region_display_name = "FilesystemAccess"
    root_path = "/home/juergen/Desktop/si_test/test"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FilesystemAccess, self).__init__(shape, uuid, "res/file_manager.png", FilesystemAccess.regiontype, FilesystemAccess.regionname, kwargs)
        self.path = FilesystemAccess.root_path
        self.color = PySI.Color(164, 216, 216, 255)
        self.qml_path = self.set_QML_path("FilesystemAccess.qml")

        if "DRAWN" in kwargs.keys() and kwargs["DRAWN"]:
            if not self.path in [r.path for r in self.current_regions() if r.regionname == FolderBubble.regionname or r.regionname == FolderIcon.regionname]:
                self.create_region_via_name(self.shape, FolderBubble.regionname, False, {"parent": None, "path": self.path, "open": False, "hierarchy_level": 0, "root": True, "root_path": self.path})
        self.delete()
