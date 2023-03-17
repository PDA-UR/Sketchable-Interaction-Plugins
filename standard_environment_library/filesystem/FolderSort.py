from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class FolderSort(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FolderSort __"
    region_display_name = "FolderSort"

    SORT_BY_NAME_ASC = 0
    SORT_BY_NAME_DSC = 1
    SORT_BY_DATE_ASC = 2
    SORT_BY_DATE_DSC = 3
    SORT_BY_ADDITION_TIME_ASC = 4
    SORT_BY_ADDITION_TIME_DSC = 5
    SORT_BY_FILE_TYPE = 6

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FolderSort, self).__init__(shape, uuid, "res/sort_icon.png", FolderSort.regiontype, FolderSort.regionname, kwargs)
        self.qml_path = self.set_QML_path("FolderSort.qml")

        self.sort_modes = {
            "Name ↑": FolderSort.SORT_BY_NAME_ASC,
            "Name ↓": FolderSort.SORT_BY_NAME_DSC,
            "Date ↑": FolderSort.SORT_BY_DATE_ASC,
            "Date ↓": FolderSort.SORT_BY_DATE_DSC,
            "Addition Time ↑": FolderSort.SORT_BY_ADDITION_TIME_ASC,
            "Addition Time ↓": FolderSort.SORT_BY_ADDITION_TIME_DSC,
            "File Type": FolderSort.SORT_BY_FILE_TYPE
        }

        self.is_popup_shown = False

        cw, ch = self.context_dimensions()

        x, y = self.aabb[0].x, self.aabb[0].y
        w, h = 300 * cw / 1920, 40 * ch / 1080

        self.shape = PySI.PointVector([[x, y], [x, y + h], [x + w, y + h], [x + w, y]])

        self.set_QML_data("widget_width", w, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", h, PySI.DataType.FLOAT)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        self.is_popup_shown = self.get_QML_data("down", PySI.DataType.BOOL)

    @SIEffect.on_continuous("__SORT_TARGET__", SIEffect.EMISSION)
    def on_sort_target_continuous_emit(self, other: object) -> None:
        key = self.get_QML_data("text", PySI.DataType.STRING)
        return FolderSort.SORT_BY_NAME_ASC if key == "" else self.sort_modes[key]
