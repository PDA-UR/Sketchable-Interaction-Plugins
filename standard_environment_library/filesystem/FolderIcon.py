from libPySI import PySI

from plugins.standard_environment_library._standard_behaviour_mixins.Transportable import Transportable
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.Folder import Folder
from plugins.standard_environment_library.filesystem import FolderBubble
from plugins.standard_environment_library.filesystem import InteractionPriorization
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
        self.is_initial = False if "is_initial" not in kwargs else kwargs["is_initial"]
        self.is_blocked = False

        if "morphed" not in kwargs or not kwargs["morphed"]:
            centerx, centery = self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2
            x = centerx - self.icon_width / 2
            y = centery - self.icon_height / 2 + self.text_height / 2

            self.shape = PySI.PointVector([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]])

        x, y = self.absolute_x_pos(), self.absolute_y_pos()
        self.create_region_via_class([[x, y], [x, y + 4], [x + 4, y + 4], [x + 4, y]], InteractionPriorization, {"parent": self})
        self.prio = None

    @SIEffect.on_enter("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_enter_emit(self, other):
        if not self.is_under_user_control and other.is_under_user_control:
            self.set_QML_data("is_highlighted", True, PySI.DataType.BOOL)

    @SIEffect.on_leave("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_leave_emit(self, other):
        self.set_QML_data("is_highlighted", False, PySI.DataType.BOOL)

    @SIEffect.on_continuous("ADD_TO_FOLDERICON", SIEffect.EMISSION)
    def on_add_to_folder_continuous_emit(self, other):
        if other.regionname != "__ InteractionPriorization __" and not self.is_blocked:
            cursor = [r for r in self.current_regions() if r.regionname == PySI.EffectName.SI_STD_NAME_MOUSE_CURSOR][0]

            if other in cursor.ctrl_selected and not cursor.ctrl_pressed and not other.is_under_user_control:
                for r in cursor.ctrl_selected:
                    r.remove_link(cursor._uuid, PySI.LinkingCapability.POSITION, r._uuid, PySI.LinkingCapability.POSITION)
                    r.move(other.absolute_x_pos() - r.absolute_x_pos() + r.x, other.absolute_y_pos() - r.absolute_y_pos() + r.y)
                    r.is_under_user_control = False

                for r in cursor.ctrl_selected:
                    if r.path != "":
                        self.add(r)
                    else:
                        new_path = self.handle_duplicate_renaming(r)
                        if r.regionname == FolderIcon.regionname:
                            os.mkdir(new_path)
                        else:
                            open(new_path, 'w').close()

                    r.remove()

                cursor.ctrl_selected = []

            if other.is_ready and other != self.parent and other.parent != self and other.path != "":
                if not self.is_under_user_control and not other.is_under_user_control and other.was_moved():
                    if hasattr(other, "prio"):
                        collisions = [uuid for uuid, name in other.present_collisions()]
                        regions = [r for r in other.current_regions() if r._uuid in collisions]
                        regions = [r for r in regions if r.regionname == FolderBubble.FolderBubble.regionname or r.regionname == FolderIcon.regionname]
                        regions = [r for r in regions if r.parent_level == max(regions, key=lambda x: x.parent_level).parent_level]

                        if len(regions) == 1:
                            self.add(other)
                        else:
                            if other.prio.folder_regionname == FolderIcon.regionname:
                                if other.prio.folder_path == self.path:
                                    self.add(other)
                    else:
                        self.add(other)

            if other.is_ready and other != self.parent and other.parent != self and other.parent == None and other.path == "":
                if not self.is_under_user_control and not other.is_under_user_control and other.was_moved():
                    self.create_add(other)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        container_width = self.get_QML_data("container_width", PySI.DataType.FLOAT)
        container_height = self.get_QML_data("container_height", PySI.DataType.FLOAT)

        if container_width != 0 and container_height != 0:
            if self.is_new([container_width, container_height], ["container_width", "container_height"]):
                self.shape = PySI.PointVector(
                    [[self.aabb[0].x, self.aabb[0].y],
                     [self.aabb[0].x, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y + container_height],
                     [self.aabb[0].x + container_width, self.aabb[0].y]
                     ]
                )

                self.width = int(container_width)
                self.height = int(container_height)

                self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
                self.set_QML_data("height", self.height, PySI.DataType.INT)

                self.is_ready = True

                if self.parent is not None and self.path != "":
                    centerx, centery = self.parent.aabb[0].x + (self.parent.aabb[3].x - self.parent.aabb[0].x) / 2, self.parent.aabb[0].y + (self.parent.aabb[1].y - self.parent.aabb[0].y) / 2
                    self.prio.move(self.absolute_x_pos() - self.prio.absolute_x_pos(), self.absolute_y_pos() - self.prio.absolute_y_pos())
                    self.move(self.parent.x + centerx - self.aabb[0].x - self.width / 2, centery - self.aabb[0].y - self.height / 2 + self.parent.y)
        else:
            self.width = int(self.icon_width * 2)
            self.height = int(self.icon_height * 2)
            self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
            self.set_QML_data("height", self.height, PySI.DataType.INT)

        fname = self.get_QML_data("text", PySI.DataType.STRING)
        if self.is_new([fname], ["text"]):
            if fname != "":
                self.entryname = fname
                self.set_QML_data("name", fname, PySI.DataType.STRING)

                if self.parent is not None or self.path != "":
                    new_path = self.path[:self.path.rfind("/") + 1] + fname
                    os.rename(self.path, new_path)
                    self.path = new_path

    @SIEffect.on_enter("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_enter_recv(self, entry_search):
        if entry_search not in self.colliding_entry_searches:
            self.colliding_entry_searches.append(entry_search)

    @SIEffect.on_continuous("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_continuous_recv(self, entry_search, query):
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
        if not self.is_blocked:

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
                    other.remove()

    def create_add(self, other):
        if not self.is_blocked:
            if other.regionname == FolderIcon.regionname or other.regionname == FolderBubble.FolderBubble.regionname:
                if other.entryname == "":
                    other.entryname = "untitled folder"
                path = self.handle_duplicate_renaming(other)
                os.mkdir(path)
            else:
                if other.entryname == "":
                    other.entryname = "new file.txt"
                path = self.handle_duplicate_renaming(other)
                open(path, 'w').close()
            other.remove()

    def handle_duplicate_renaming(self, other):
        new_path = self.path + "/" + other.entryname

        while os.path.exists(new_path):
            if other.regionname == FolderIcon.regionname or other.regionname == FolderBubble.FolderBubble.regionname:
                other.entryname += "_other"
            else:
                ext = other.entryname[other.entryname.rfind(".") + 1:]
                other.entryname = other.entryname[:other.entryname.rfind(f".{ext}")] + "_other" + f".{ext}" if ext != "" else ""
            new_path = self.path + "/" + other.entryname

        other.set_QML_data("name", other.entryname, PySI.DataType.STRING)

        return new_path

    def on_double_clicked(self):
        self.morph()
        return True

    def compute_morph_coordinates(self):
        centerx, centery = self.x + self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.y + self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2
        x = centerx - self.icon_width / 2
        y = centery - self.icon_height / 2
        return x, y, centerx, centery

    def morph(self):
        x, y, centerx, centery = self.compute_morph_coordinates()
        kwargs = {}
        kwargs["parent"] = self.parent if self.parent is not None else None
        kwargs["path"] = self.path
        kwargs["center"] = centerx, centery
        kwargs["entryname"] = self.entryname
        kwargs["is_morphed"] = True
        self.remove()
        if self.parent is not None:
            if self in self.parent.linked_content:
                self.parent.linked_content.remove(self)
        self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]], FolderBubble, kwargs)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    def remove(self):
        self.prio.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.prio._uuid, PySI.LinkingCapability.POSITION)
        self.prio.delete()
        super().remove()