from libPySI import PySI
from plugins.standard_environment_library.filesystem.Entry import Entry
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class TextFile(Entry):
    regiontype = PySI.EffectType.SI_TEXT_FILE
    regionname = PySI.EffectName.SI_STD_NAME_TEXTFILE

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(TextFile, self).__init__(shape, uuid, TextFile.regiontype, TextFile.regionname, kwargs)
        self.qml_path = self.set_QML_path("TextFile.qml")

        self.set_QML_data("text_height", self.text_height, PySI.DataType.INT)
        self.set_QML_data("img_path", "res/file_icon.png", PySI.DataType.STRING)

    @SIEffect.on_enter(E.capability.tag_tagging, SIEffect.RECEPTION)
    def on_tag_enter_recv(self):
        self.set_QML_data("visible", True, PySI.DataType.BOOL)
