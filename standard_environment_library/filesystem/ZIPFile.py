from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.File import File
from plugins.E import E


class ZIPFile(File):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ZIPFile __"
    region_display_name = "ZIPFile"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(ZIPFile, self).__init__(shape, uuid, "res/file_icon.png", ZIPFile.regiontype, ZIPFile.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.qml_path = self.set_QML_path("ZIPFile.qml")
        self.border_width = 2
        self.is_text: SIEffect.SI_CONDITION = True

        self.set_QML_data("icon_view", True, PySI.DataType.BOOL)

    def on_double_clicked(self):
        pass