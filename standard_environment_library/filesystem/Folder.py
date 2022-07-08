from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.FilesystemEntry import FilesystemEntry
from plugins.E import E
import shutil


class Folder(FilesystemEntry):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Folder __"
    region_display_name = "Folder"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ Folder __", kwargs: dict = {}) -> None:
        super(Folder, self).__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)
        pass

    def delete_from_disk(self):
        shutil.rmtree(self.path, True)