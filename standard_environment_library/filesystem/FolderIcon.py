from libPySI import PySI

from plugins.standard_environment_library._standard_behaviour_mixins.Transportable import Transportable
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.Folder import Folder
from plugins.standard_environment_library.filesystem import FolderBubble
from plugins.E import E
import os
from iteration_utilities import flatten


class FolderIcon(Transportable, Folder):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ FolderIcon __"
    region_display_name = "FolderIcon"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FolderIcon, self).__init__(shape, uuid, "res/dir.png", FolderIcon.regiontype, FolderIcon.regionname, kwargs)
        self.qml_path = self.set_QML_path("FolderIcon.qml")
        self.is_folder: SIEffect.SI_CONDITION = True
        self.colliding_entry_searches = []

    @SIEffect.on_enter("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_enter_emit(self, other):
        if not self.is_under_user_control and other.is_under_user_control:
            self.set_QML_data("is_highlighted", True, PySI.DataType.BOOL)

    @SIEffect.on_leave("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_leave_emit(self, other):
        self.set_QML_data("is_highlighted", False, PySI.DataType.BOOL)

    @SIEffect.on_continuous("ADD_TO_FOLDERICON", SIEffect.EMISSION)
    def on_add_to_folder_continuous_emit(self, other):
        if other.is_ready and other != self.parent and other.parent != self:
            if not self.is_under_user_control and not other.is_under_user_control and other.was_moved():
                self.add(other)

    @SIEffect.on_enter("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_enter_recv(self, entry_search):
        if entry_search not in self.colliding_entry_searches:
            self.colliding_entry_searches.append(entry_search)

    @SIEffect.on_continuous("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_continuous_recv(self, entry_search, query, change):
        if change:
            self.visualize_search_count(entry_search, query)

    def visualize_search_count(self, entry_search, query):
        self.set_QML_data("search_hit_count_visible", False, PySI.DataType.BOOL)

        queries = [query]
        c = list(flatten([fname for dp, dn, fname in os.walk(self.path)]))

        for es in self.colliding_entry_searches:
            if es == entry_search:
                continue

            queries += [es.current_query]

        res = []
        for q in queries:
            res.append([])
            for s in c:
                if q in s:
                    res[-1].append(s)

        ret = []
        if len(res) > 0:
            ret = set(res[0])
            for i in range(1, len(res)):
                ret &= set(res[i])

        ret = len(list(ret))

        if ret > 0:
            self.set_QML_data("is_greyed_out", False, PySI.DataType.BOOL)
            self.set_QML_data("search_hit_count", str(ret), PySI.DataType.STRING)
            self.set_QML_data("search_hit_count_visible", True, PySI.DataType.BOOL)

    @SIEffect.on_leave("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_leave(self, entry_search, query):
        if entry_search in self.colliding_entry_searches:
            self.colliding_entry_searches.remove(entry_search)

    def add(self, other):
        if os.path.commonprefix([self.path, other.path]) != other.path:
            new_path = self.path + "/" + other.entryname
            os.rename(other.path, new_path)
            if other.parent is not None:
                if other in other.parent.linked_content:
                    other.parent.linked_content.remove(other)
                other.remove_link(other.parent._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

            if other.regionname == FolderBubble.FolderBubble.regionname:
                other.remove()
            else:
                other.delete()

    def on_double_clicked(self):
        self.morph()
        return True

    def compute_morph_coordinates(self):
        centerx, centery = self.x + self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.y + self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2
        x = centerx - self.icon_width / 2
        y = centery - self.icon_height / 2
        return x, y, centerx, centery

    def morph(self):
        centerx, centery = self.x + self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.y + self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2
        x, y, centerx, centery = self.compute_morph_coordinates()
        kwargs = {}
        kwargs["parent"] = self.parent if self.parent is not None else None
        kwargs["path"] = self.path
        kwargs["center"] = centerx, centery
        kwargs["entryname"] = self.entryname
        self.delete()
        if self.parent is not None:
            if self in self.parent.linked_content:
                self.parent.linked_content.remove(self)
        self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]], FolderBubble, kwargs)