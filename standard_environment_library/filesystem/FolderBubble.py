from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.Folder import Folder
from plugins.standard_environment_library.filesystem import TextFile
from plugins.standard_environment_library.filesystem import PDFFile
from plugins.standard_environment_library.filesystem import ZIPFile
from plugins.standard_environment_library.filesystem import ImageFile
from plugins.standard_environment_library.filesystem import FolderIcon
from plugins.standard_environment_library.filesystem.FolderSort import FolderSort
from plugins.standard_environment_library.email import InboxItem
from plugins.E import E
from iteration_utilities import flatten

import numpy as np
import splines
import glob
import os
from datetime import datetime


class FolderBubble(Folder):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FolderBubble __"
    region_display_name = "FolderBubble"
    SORTING_MODE_ASCENDING = False
    SORTING_MODE_DESCENDING = True
    SORTING_CRITERIA_NAME = 0
    SORTING_CRITERIA_SEQUENCE = 1
    SORTING_CRITERIA_DATE = 2
    SORTING_CRITERIA_FILE_TYPE = 3
    SORTING_CRITERIA_DEFAULT = SORTING_CRITERIA_NAME
    SORTING_MODE_DEFAULT = SORTING_MODE_ASCENDING

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FolderBubble, self).__init__(shape, uuid, "", FolderBubble.regiontype, FolderBubble.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.with_border = True
        self.default_with_border = True
        self.qml_path = self.set_QML_path("FolderBubble.qml")
        self.image_file_extensions = [".png", ".jpeg", ".jpg"]
        self.text_file_extensions = [".txt", ".md", ".py", ".tex"]
        self.pdf_file_extension = ".pdf"
        self.zip_file_extension = ".zip"
        self.mail_file_extensions = ["Mail:"]
        self.start_center = None if "center" not in kwargs else kwargs["center"]
        self.content = self.__fetch_contents__()
        self.linked_content = []
        self.color = PySI.Color(250, 132, 43, 255)
        self.grey_out_color = PySI.Color(132, 132, 132, 63)
        self.default_color = PySI.Color(250, 132, 43, 255)
        self.highlight_color = PySI.Color(0, 120, 215, 255)
        self.border_width = int(8 * cw / 1920)
        self.default_border_color = PySI.Color(72, 79, 81, 255)
        self.border_color = self.default_border_color
        self.entry_spacing_offset = cw / 750
        self.parent_level = 0
        self.set_QML_data("widget_width", int(self.aabb[3].x - self.aabb[0].x), PySI.DataType.FLOAT)
        self.set_QML_data("height", int(self.aabb[1].y - self.aabb[0].y), PySI.DataType.INT)
        self.set_QML_data("name", self.entryname, PySI.DataType.STRING)
        self.morph_entryname = "" if "entryname" not in kwargs else kwargs["entryname"]
        self.is_split = False if "is_split" not in kwargs else kwargs["is_split"]
        self.colliding_entry_searches = []
        self.last_recv_sort_mode = -1
        self.last_used_sort_criteria = FolderBubble.SORTING_CRITERIA_DEFAULT
        self.last_used_sort_criteria_mode = FolderBubble.SORTING_MODE_DEFAULT

    def adjust_color(self):
        self.parent_level = 0 if self.parent is None else self.num_parents()

        if self.parent_level > 0:
            r = self.default_color.r
            g = self.default_color.g
            b = self.default_color.b
            for i in range(self.parent_level):
                r = r + (255 - r) * 1 / 6
                g = g + (255 - g) * 1 / 6
                b = b + (255 - b) * 1 / 6

            self.color = PySI.Color(r, g, b, 255)
            self.default_color = PySI.Color(r, g, b, 255)

    def num_parents(self):
        if self.parent is None:
            return 0

        s = 0
        parent = self.parent

        while parent is not None:
            s += 1
            parent = parent.parent

        return s

    def search(self, query, is_case_sensitive=False):
        # return list of entries which do NOT match query
        # these entries then are greyed out
        return [lc for lc in self.linked_content if query.lower() not in lc.entryname.lower()] if is_case_sensitive else [lc for lc in self.linked_content if query not in lc.entryname]

    @SIEffect.on_enter("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_enter_recv(self, entry_search):
        if entry_search not in self.colliding_entry_searches:
            self.colliding_entry_searches.append(entry_search)

    @SIEffect.on_continuous("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_continuous_recv(self, entry_search, query, change):
        if change:
            self.remove_grey_out(entry_search, query)
            self.grey_out(entry_search, query)

    @SIEffect.on_leave("__MATCH_ENTRIES__", SIEffect.RECEPTION)
    def on_match_entries_leave(self, entry_search, query):
        if entry_search in self.colliding_entry_searches:
            self.colliding_entry_searches.remove(entry_search)
        self.remove_grey_out(entry_search, query)

    def remove_grey_out(self, entry_search, query):
        for lc in self.linked_content:
            lc.set_QML_data("is_greyed_out", False, PySI.DataType.BOOL)
            lc.set_QML_data("search_hit_count_visible", False, PySI.DataType.BOOL)

            if lc.regionname == FolderBubble.regionname:
                lc.color = lc.default_color
                lc.border_color = lc.default_border_color
                lc.remove_grey_out(entry_search, query)
                lc.grey_out(entry_search, query)

            if lc.regionname == FolderIcon.FolderIcon.regionname and query != "":
                lc.visualize_search_count(entry_search, query)

    def ANDing_of_concurrent_search_queries_results(self, entry_search, last_updated_query):
        targets = self.search(last_updated_query)
        for es in self.colliding_entry_searches:
            if es == entry_search:
                continue
            targets += self.search(es.current_query)

        return list(set(targets))

    def grey_out(self, entry_search, query):
        for t in self.ANDing_of_concurrent_search_queries_results(entry_search, query):
            t.set_QML_data("is_greyed_out", True, PySI.DataType.BOOL)

            if t.regionname == FolderIcon.FolderIcon.regionname:
                t.visualize_search_count(entry_search, query)

            if t.regionname == FolderBubble.regionname:
                t.color = t.grey_out_color
                t.border_color = t.grey_out_color
                t.grey_out(entry_search, query)

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        self.is_ready = True
        centerx, centery = self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2

        x = centerx - self.icon_width / 2 + self.x
        y = centery - self.icon_height / 2 + self.y

        if self.path == "":
            self.entryname = self.morph_entryname
            self.set_QML_data("name", self.entryname, PySI.DataType.STRING)
            return

        self.set_QML_data("name", self.entryname, PySI.DataType.STRING)

        self.adjust_color()

        for c in self.content:
            kwargs = {}
            kwargs["parent"] = self
            kwargs["path"] = c[0]
            kwargs["parent_level"] = self.parent_level + 1
            kwargs["root_path"] = self.root_path

            if getattr(c[1], c[1].__si_name__).regionname == InboxItem.InboxItem.regionname:
                f = open(c[0])
                sender, receiver, subject, message, date, is_unread = f.readlines()
                kwargs["data"] = {
                    "email_sender": sender[:-1],
                    "email_receiver": receiver[:-1],
                    "email_subject": subject[:-1],
                    "message": message[:-1],
                    "date": date[:-1],
                    "is_unread": eval(is_unread)
                }
                f.close()

            self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width * 2, y + self.icon_height], [x + self.icon_width * 2, y]], c[1], kwargs)

        self.set_QML_data("img_path", "", PySI.DataType.STRING)

    def __fetch_contents__(self) -> list:
        return [(entry, FolderIcon if os.path.isdir(entry) else ZIPFile if entry[entry.rfind("."):] == self.zip_file_extension else PDFFile if entry[entry.rfind("."):] == self.pdf_file_extension else TextFile if entry[entry.rfind("."):] in self.text_file_extensions else ImageFile if entry[entry.rfind("."):] in self.image_file_extensions else InboxItem if entry[entry.rfind("/") + 1:entry.rfind(":")+1] in self.mail_file_extensions else TextFile) for entry in glob.glob(self.path + "/*")]

    def on_double_clicked(self):
        self.morph()
        return True

    def remove(self, recurse=True):
        self.delete()
        self.is_removed = True

        for lc in self.linked_content:
            self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, lc._uuid, PySI.LinkingCapability.POSITION)

            if lc.regionname == FolderBubble.regionname:
                lc.remove(False)

            lc.delete()
            lc.is_removed = True

        self.linked_content.clear()

        if self.parent is not None and recurse:
            if self in self.parent.linked_content:
                self.parent.linked_content.remove(self)

    def morph(self):
        self.remove()

        centerx, centery = self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2

        x = centerx - self.icon_width / 2 + self.x
        y = centery - self.icon_height / 2 + self.y

        kwargs = {}
        kwargs["parent"] = self.parent
        kwargs["path"] = self.path
        kwargs["morphed"] = True

        self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width * 2, y + self.icon_height], [x + self.icon_width * 2, y]], FolderIcon, kwargs)

    def expand(self):
        movements, grid_pts = self.to_grid()
        if len(movements) != 0 and len(grid_pts) != 0:
            centerx, centery = self.absolute_x_pos() + 0.5 * self.width, self.absolute_y_pos() + 0.5 * self.height

            for t, move in zip(self.linked_content, movements):
                t.move(self.x + t.x + move[0], self.y + t.y + move[1])

                if t.regionname == FolderBubble.regionname:
                    t.emit_linking_action(t._uuid, PySI.LinkingCapability.POSITION, t.position())

            exploded = self.explode(grid_pts, 0.9)
            shape = self.splines(exploded)
            self.shape = PySI.PointVector(shape)
            self.set_QML_data("widget_width", int(self.aabb[3].x - self.aabb[0].x), PySI.DataType.FLOAT)
            self.set_QML_data("height", int(self.aabb[1].y - self.aabb[0].y), PySI.DataType.INT)
            self.width = int(self.aabb[3].x - self.aabb[0].x)
            self.height = int(self.aabb[1].y - self.aabb[0].y)

            ncenterx, ncentery = self.absolute_x_pos() + 0.5 * self.width, self.absolute_y_pos() + 0.5 * self.height
            self.move(self.x - (ncenterx - centerx), self.y - (ncentery - centery))
            self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, self.position())

        if self.parent is not None:
            self.parent.expand()

    def splines(self, pts):
        spline = splines.CatmullRom(pts, endconditions='closed')
        dots_per_second = 10
        total_duration = spline.grid[-1] - spline.grid[0]
        dots = int(total_duration * dots_per_second) + 1
        times = spline.grid[0] + np.arange(dots) / dots_per_second
        result = spline.evaluate(times).T

        return [[result[0][i], result[1][i]] for i in range(len(result[0]))]

    def compute_center(self, points):
        return sum([p[0] for p in points]) / len(points), sum([p[1] for p in points]) / len(points)

    def explode(self, points, factor):
        cx, cy = self.compute_center(points)

        for p in points:
            p[0] = cx + (p[0] - cx) * factor
            p[1] = cy + (p[1] - cy) * factor

        return points

    def grid_dimensions(self, n, max_cols=3):
        rows = int(n / max_cols) + 1 if n % max_cols != 0 else int(n / max_cols)
        rows = rows if rows != 0 else 1
        cols = n / rows
        return rows, int(cols) if cols.is_integer() else int(cols) + 1

    def build_movement_list(self, offset, lc):
        rows, cols = self.grid_dimensions(len(lc))
        moves = []
        y = self.aabb[0].y + self.y
        ty = 0
        for row in range(rows):
            x = self.aabb[0].x + self.x
            for col in range(cols):
                i = row * cols + col
                if i == len(lc):
                    break
                target = lc[i]
                moves.append((target, x, y, x + target.width, y + target.height))
                x += offset + target.width
                ty = max(ty, target.height + offset)
            y += ty

        if len(moves) == 0:
            return [], []

        minx = min(moves, key=lambda t: t[1])[1]
        miny = min(moves, key=lambda t: t[2])[2]
        maxx = max(moves, key=lambda t: t[3])[3]
        maxy = max(moves, key=lambda t: t[4])[4]

        return [(x - target.absolute_x_pos(), y - target.absolute_y_pos()) for target, x, y, _, _ in moves], [[minx, miny], [minx, maxy], [maxx, maxy], [maxx, miny]]

    def sort_by(self, criteria, mode):
        if criteria == FolderBubble.SORTING_CRITERIA_NAME:
            return sorted(self.linked_content, key=lambda x: x.entryname, reverse=mode)
        elif criteria == FolderBubble.SORTING_CRITERIA_DATE:
            return sorted(self.linked_content, key=lambda x: x.creation_time, reverse=mode)
        elif criteria == FolderBubble.SORTING_CRITERIA_SEQUENCE:
            return sorted(self.linked_content, key=lambda x: x.parenting_time, reverse=mode)
        elif criteria == FolderBubble.SORTING_CRITERIA_FILE_TYPE:
            return sorted(self.linked_content, key=lambda x: x.regionname)

    def sort_linked_content(self):
        self.linked_content = self.sort_by(self.last_used_sort_criteria, self.last_used_sort_criteria_mode)

    def to_grid(self):
        self.sort_linked_content()
        movements, dimensions = self.build_movement_list(self.entry_spacing_offset, self.linked_content)
        return movements, dimensions

    def add_entry(self, other):
        if not self.is_under_user_control and not other.is_under_user_control:
            other.parenting_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            self.linked_content.append(other)
            other.parent_level = self.parent_level + 1
            if other.regionname == InboxItem.InboxItem.regionname:
                f = open(other.path, 'w')
                f.write(other.email_sender + "\n" +
                    other.email_receiver + "\n" +
                    other.email_subject + "\n" +
                    other.email_message + "\n" +
                    other.datetime + "\n" +
                    str(other.is_unread))
                f.close()

            if len(self.linked_content) == len(self.content):
                self.expand()

    def prepare_drawn_entry_addition(self, other):
        other.path = self.path + "/" + other.entryname

        if other.regionname == FolderIcon.FolderIcon.regionname or other.regionname == FolderBubble.regionname:
            self.prepare_drawn_folder_addition(other)
        else:
            self.prepare_drawn_file_addition(other)

    def handle_duplicate_renaming(self, other):
        new_path = self.path + "/" + other.entryname

        if other.entryname in [e.entryname for e in self.linked_content]:
            while os.path.exists(new_path):
                if other.regionname == FolderIcon.FolderIcon.regionname or other.regionname == FolderBubble.regionname:
                    other.entryname += "_other"
                else:
                    ext = other.entryname[other.entryname.rfind(".") + 1:]
                    other.entryname = other.entryname[:other.entryname.rfind(f".{ext}")] + "_other" + f".{ext}" if ext != "" else ""
                new_path = self.path + "/" + other.entryname

        other.set_QML_data("name", other.entryname, PySI.DataType.STRING)
        self.parent_to(other)

        return new_path

    def prepare_drawn_folder_addition(self, other):
        new_path = self.handle_duplicate_renaming(other)
        other.path = new_path
        os.mkdir(other.path)
        self.parent_to(other)

    def prepare_drawn_file_addition(self, other):
        if other.regionname == InboxItem.InboxItem.regionname:
            f = open(other.path, 'w')
            f.write(other.email_sender + "\n" +
                    other.email_receiver + "\n" +
                    other.email_subject + "\n" +
                    other.email_message + "\n" +
                    str(other.is_unread))
            f.close()
        else:
            new_path = self.handle_duplicate_renaming(other)
            other.path = new_path
            open(other.path, 'w').close()

    def parent_to(self, other):
        self.content = self.__fetch_contents__()
        other.parent = self
        other.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)

    def adjust_linked_content_paths(self):
        for e in self.linked_content:
            e.path = self.path + "/" + e.entryname

            if e.regionname == FolderBubble.regionname:
                e.adjust_linked_content_paths()

    def prepare_existing_entry_addition(self, other):
        if os.path.commonprefix([self.path, other.path]) != other.path:
            new_path = self.handle_duplicate_renaming(other)
            os.rename(other.path, new_path)
            other.path = new_path

            if other.regionname == FolderBubble.regionname:
                other.adjust_linked_content_paths()

            self.parent_to(other)

    def prepare_existing_entry_inner_addition(self, other):
        if other in other.parent.linked_content:
            other.parent.linked_content.remove(other)
            other.remove_link(other.parent._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
            # other.parent.expand()
            other.parent = None

    def add(self, other):
        if other.is_ready and other.parent == self:
            self.add_entry(other)
        elif other.is_ready and other.parent is None and other.path != self.root_path:
            if other.entryname == "":
                return
            if not self.is_under_user_control and not other.is_under_user_control:
                if other.path == "":
                    self.prepare_drawn_entry_addition(other)
                else:
                    self.prepare_existing_entry_addition(other)
        elif other.is_ready and other.parent is not None:
            if not self.is_under_user_control and other.is_under_user_control:
                self.prepare_existing_entry_inner_addition(other)

    @SIEffect.on_continuous("ADD_TO_FOLDERBUBBLE", SIEffect.EMISSION)
    def on_add_to_folder_continuous_emit(self, other):
        if other not in self.linked_content:
            self.add(other)

    @SIEffect.on_leave("ADD_TO_FOLDERBUBBLE", SIEffect.EMISSION)
    def on_add_to_folder_leave_emit(self, other):
        if other in self.linked_content and other.is_under_user_control:
            self.linked_content.remove(other)
            other.parent = None
            other.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
            self.expand()

    @SIEffect.on_continuous("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_continuous_emit(self, other):
        if other.is_under_user_control:
            self.evaluate_highlighting(other)
        else:
            self.evaluate_unhighlighting(other)

    def evaluate_highlighting(self, other):
        if len([r[0] for r in other.present_collisions() if r[1] == FolderIcon.FolderIcon.regionname]) > 0:
            self.unhighlight()
            return

        folders = [(r, r.parent_level) for r in self.current_regions() if r.regionname == FolderBubble.regionname]
        folders.sort(key=lambda tup: tup[1], reverse=True)
        collisions = [r[0] for r in other.present_collisions() if r[1] == FolderBubble.regionname]

        uid = self.target_uuid(folders, collisions)
        self.unhighlight_non_self_folders(folders, uid)

        if self._uuid == uid:
            self.highlight(other)

    def evaluate_unhighlighting(self, other):
        if other.was_moved():
            self.unhighlight()

    def unhighlight(self):
        self.border_color = self.default_border_color
        self.color = self.default_color

    def highlight(self, other):
        if other.enveloped_by(self):
            self.color = self.highlight_color
            self.border_color = self.default_border_color
        else:
            self.border_color = self.highlight_color
            self.color = self.default_color

    def unhighlight_non_self_folders(self, folders, uid):
        for f in folders:
            if f[0]._uuid != uid:
                f[0].color = f[0].default_color
                f[0].border_color = f[0].default_border_color

    def target_uuid(self, folders, collisions):
        for f in folders:
            if f[0]._uuid in collisions:
                return f[0]._uuid

        return ""

    @SIEffect.on_leave("__HIGHLIGHT_ADDITION__", SIEffect.EMISSION)
    def on_highlight_addition_leave_emit(self, other):
        self.color = self.default_color
        self.border_color = self.default_border_color

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_continuous("__SORT_TARGET__", SIEffect.RECEPTION)
    def on_sort_target_continuous_recv(self, sort_mode) -> None:
        if sort_mode != self.last_recv_sort_mode:
            self.last_recv_sort_mode = sort_mode
            self.last_used_sort_criteria, self.last_used_sort_criteria_mode = self.update_sort_mode()
            self.expand()

    def update_sort_mode(self):
        if self.last_recv_sort_mode == FolderSort.SORT_BY_NAME_ASC:
            return FolderBubble.SORTING_CRITERIA_NAME, FolderBubble.SORTING_MODE_ASCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_NAME_DSC:
            return FolderBubble.SORTING_CRITERIA_NAME, FolderBubble.SORTING_MODE_DESCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_DATE_ASC:
            return FolderBubble.SORTING_CRITERIA_DATE, FolderBubble.SORTING_MODE_ASCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_DATE_DSC:
            return FolderBubble.SORTING_CRITERIA_DATE, FolderBubble.SORTING_MODE_DESCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_ADDITION_TIME_ASC:
            return FolderBubble.SORTING_CRITERIA_SEQUENCE, FolderBubble.SORTING_MODE_ASCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_ADDITION_TIME_DSC:
            return FolderBubble.SORTING_CRITERIA_SEQUENCE, FolderBubble.SORTING_MODE_DESCENDING
        elif self.last_recv_sort_mode == FolderSort.SORT_BY_FILE_TYPE:
            return FolderBubble.SORTING_CRITERIA_FILE_TYPE, FolderBubble.SORTING_MODE_ASCENDING