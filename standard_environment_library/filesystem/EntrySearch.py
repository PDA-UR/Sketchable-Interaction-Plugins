from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class EntrySearch(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ EntrySearch __"
    region_display_name = "EntrySearch"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(EntrySearch, self).__init__(shape, uuid, "res/search.png", EntrySearch.regiontype, EntrySearch.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.qml_path = self.set_QML_path("EntrySearch.qml")
        self.color = PySI.Color(0, 255, 0, 255)
        self.current_query = ""

        x, y = self.aabb[0].x, self.aabb[0].y
        w, h = 300 * cw / 1920, 40 * ch / 1080

        self.shape = PySI.PointVector([[x, y], [x, y + h], [x + w, y + h], [x + w, y]])

        self.set_QML_data("widget_width", w, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", h, PySI.DataType.FLOAT)

    @SIEffect.on_enter("__MATCH_ENTRIES__", SIEffect.EMISSION)
    def on_match_entries_enter(self, other):
        return self

    @SIEffect.on_continuous("__MATCH_ENTRIES__", SIEffect.EMISSION)
    def on_match_entries_continuous_emit(self, other):
        self.current_query = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)
        return self, self.current_query

    @SIEffect.on_leave("__MATCH_ENTRIES__", SIEffect.EMISSION)
    def on_match_entries_leave(self, other):
        return self, self.current_query
