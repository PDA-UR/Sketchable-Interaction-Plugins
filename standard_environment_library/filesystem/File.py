from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.FilesystemEntry import FilesystemEntry
from plugins.standard_environment_library._standard_behaviour_mixins.Transportable import Transportable
from plugins.E import E


class File(Transportable, FilesystemEntry):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ File __"
    region_display_name = "File"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ File __", kwargs: dict = {}) -> None:
        super(File, self).__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)
        pass
