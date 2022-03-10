from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.Content import Content
from plugins.E import E


class AbstractFile(Content):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ AbstractFile __"
    region_display_name = "AbstractFile"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", texture_path="", regiontype=PySI.EffectType.SI_CUSTOM_NON_DRAWABLE, regionname="__ AbstractFile __", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, texture_path, regiontype, regionname, kwargs)
        self.filename = "" if self.path == "" else self.path[self.path.rfind("/") + 1:]
        self.is_open_entry_capability_blocked = False
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", self.filename, PySI.DataType.STRING)

    def adjust_path_for_duplicate(self):
        self.path = self.root_path + "/.temp"
        n = "new_file"
        i = sum(element[index:index + len(n)] == n for element in [r.filename for r in self.current_regions() if issubclass(r.__class__, AbstractFile)] for index, char in enumerate(element))
        self.filename = n + ".txt" if i == 0 else n + f"{i+1}.txt"
        self.path += "/" + self.filename
        open(self.path, "w")

    @SIEffect.on_continuous(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.RECEPTION)
    def on_open_entry_continuous_recv(self, is_other_controlled: bool) -> None:
        if self.parent is None and not self.is_under_user_control and not is_other_controlled and not self.is_open_entry_capability_blocked:
            self.is_open_entry_capability_blocked = True
            self.start_standard_application(self._uuid, self.path)

    @SIEffect.on_leave(PySI.CollisionCapability.OPEN_ENTRY, SIEffect.RECEPTION)
    def on_open_entry_leave_recv(self, is_other_controlled: bool) -> None:
        if self.parent is None and self.is_open_entry_capability_blocked:
            self.close_standard_application(self._uuid)
            self.is_open_entry_capability_blocked = False