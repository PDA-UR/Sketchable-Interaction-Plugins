import os
from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.AbstractFile import AbstractFile
from plugins.E import E


class TextFile(AbstractFile):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__TEXT_FILE__"
    region_display_name = "Text File"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "res/file_icon.png", TextFile.regiontype, TextFile.regionname, kwargs)
        if self.path == "":
            self.adjust_path_for_duplicate()

        self.qml_path = self.set_QML_path("TextFile.qml")
        self.set_QML_data("name", self.filename, PySI.DataType.STRING)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        super().on_canvas_continuous_recv(canvas_uuid)
        self.rename()

    @SIEffect.on_enter(E.capability.tag_tagging, SIEffect.RECEPTION)
    def on_tag_enter_recv(self):
        self.set_QML_data("visible", True, PySI.DataType.BOOL)