from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem import TextFile
from plugins.standard_environment_library.filesystem import ImageFile
from plugins.standard_environment_library.filesystem import FolderIcon
from plugins.standard_environment_library.filesystem.Content import Content
from plugins.E import E

from scipy.spatial import ConvexHull

import numpy as np
import splines
import glob
import os


class Folder(Content):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Folder __"
    region_display_name = "Folder"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/dir.png", Folder.regiontype, Folder.regionname, kwargs)
        self.qml_path = self.set_QML_path("Folder.qml")
        self.color = PySI.Color(250, 132, 43, 255)
        self.default_color = PySI.Color(250, 132, 43, 255)
        self.image_file_extensions = [".png", ".jpeg", ".jpg"]
        self.text_file_extensions = [".txt", ".odt", ".md", ".pdf", ".py", ".tex"]
        self.with_border = True
        self.is_initial = True

        self.linked_content = []
        self.content = self.__fetch_contents__()
        self.expected_num_content = 0
        self.parent_level = 0
        self.is_morphed = "morphed" in kwargs and kwargs["morphed"]
        self.foldername = "" if self.path == "" else self.path[self.path.rfind("/") + 1:]
        self.is_root = "root" in kwargs and kwargs["root"]
        self.border_width = 8
        self.block_color_change = False

        self.is_selector = "is_selector" in kwargs and kwargs["is_selector"]
        self.is_drawn = "DRAWN" in kwargs and kwargs["DRAWN"]

        self.set_QML_data("name", self.foldername, PySI.DataType.STRING)
        self.set_QML_data("height", int(self.aabb[1].y - self.aabb[0].y), PySI.DataType.INT)

        # self.__notify__("HELLO WORLD", PySI.DataType.STRING)

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

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        self.adjust_color()

        if not self.is_drawn and not self.is_selector:
            centerx, centery = self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2

            x = centerx - self.icon_width / 2 + self.x
            y = centery - self.icon_height / 2 + self.y

            for c in self.content:
                kwargs = {}
                kwargs["parent"] = self
                kwargs["path"] = c[0]
                kwargs["hierarchy_level"] = self.parent_level
                kwargs["root_path"] = self.root_path

                self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]], c[1], kwargs)
        else:
            dirx, diry = self.aabb[0].x, self.aabb[0].y

            self.shape = PySI.PointVector([[dirx, diry],
                                           [dirx, diry + 133],
                                           [dirx + 89, diry + 133],
                                           [dirx + 89, diry]])

        self.set_QML_data("img_path", "", PySI.DataType.STRING)

    def on_double_clicked(self):
        self.morph()

    def remove(self, recurse=True):
        self.delete()
        self.is_removed = True

        for lc in self.linked_content:
            self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, lc._uuid, PySI.LinkingCapability.POSITION)

            if lc.regionname == Folder.regionname:
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

        self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]], FolderIcon, kwargs)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        container_width = self.get_QML_data("container_width", PySI.DataType.FLOAT)
        container_height = self.get_QML_data("container_height", PySI.DataType.FLOAT)
        self.is_drawn = False

        if self.is_new([container_width, container_height], ["container_width", "container_height"]):
            self.visualization_width = int(container_width)
            self.visualization_height = int(container_height)
            self.is_ready = True

        self.rename()

    def is_new(self, values, keys):
        is_new = False

        for v, k in zip(values, keys):
            if k not in self.__qml_data__:
                is_new = True
            else:
                if k in self.__qml_data__ and self.__qml_data__[k] != v:
                    is_new = True

            self.__qml_data__[k] = v

        return is_new

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y, {"mover": self}

    @SIEffect.on_enter("__PARENT_CONTENT__", SIEffect.EMISSION)
    def on_content_enter_emit(self, other: object) -> None:
        pass

    def remove_content_and_link(self, content):
        if content in self.linked_content:
            self.linked_content.remove(content)
        self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, content._uuid, PySI.LinkingCapability.POSITION)
        self.content = self.__fetch_contents__()

    @SIEffect.on_continuous("__PARENT_CONTENT__", SIEffect.EMISSION)
    def on_content_continuous_emit(self, other: object) -> None:
        if other not in self.linked_content:
            if other.is_removed:
                if other.regionname == FolderIcon.FolderIcon.regionname or other.regionname == Folder.regionname:
                    self.expected_num_content -= 1
                return
            if other.is_ready:
                if other.path in [c[0] for c in self.content] and other.parent is not None:
                    self.linked_content.append(other)
                    self.create_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
                    other.parent = self
                    self.expand()
                    if other.regionname == Folder.regionname:
                        other.adjust_color()
                    self.expected_num_content += 1
                # new addition; needs distinction between Folder in Folder and Addition
                else:
                    if other.was_moved():
                        if other.regionname != Folder.regionname:
                            if self.path + "/" + other.filename in [r.path for r in self.linked_content]:
                                original_path = other.path
                                fn = other.filename
                                fp = other.path
                                while fn in [r.filename if hasattr(r, "filename") else r.foldername for r in self.linked_content]:
                                    if other.regionname == FolderIcon.FolderIcon.regionname:
                                        fn += "_other"
                                        fp += "_other"
                                        other.set_QML_data("name", fp, PySI.DataType.STRING)
                                    else:
                                        fn = fn[:-4] + "_other" + fn[-4:]
                                        fp = fp[:-4] + "_other" + fp[-4:]
                                        other.set_QML_data("name", fn, PySI.DataType.STRING)

                                os.rename(original_path, fp)
                                other.filename = fn
                                other.path = fp
                        else:
                            if self.path + "/" + other.foldername in [r.path for r in self.linked_content]:
                                original_path = other.path
                                while other.foldername in [r.filename if hasattr(r, "filename") else r.foldername for r in self.linked_content]:
                                    other.foldername += "_other"
                                    other.path += "_other"
                                    other.set_QML_data("name", other.path, PySI.DataType.STRING)

                                os.rename(original_path, other.path)

                                def rename_folder_content(o):
                                    for lc in o.linked_content:
                                        if lc.regionname == Folder.regionname:
                                            lc.path = o.path + "/" + lc.foldername
                                            lc.set_QML_data("name", lc.path, PySI.DataType.STRING)
                                            rename_folder_content(lc)
                                        else:
                                            lc.path = o.path + "/" + lc.filename

                                            if lc.regionname == FolderIcon.FolderIcon.regionname:
                                                lc.set_QML_data("name", lc.path, PySI.DataType.STRING)

                                rename_folder_content(other)

                        if other.regionname == Folder.regionname and not other.is_root and not other.path == self.root_path:
                            if other.enveloped_by(self):
                                # addition
                                if other.parent is None and other.parent != self and self.parent != other:
                                    self.move_content_to_folder(other)
                                    self.expand()
                                    self.expected_num_content += 1
                                    other.adjust_color()
                                # from outer folder to inner folder
                                elif other.parent is not None and self.parent is not None and other.parent == self.parent:
                                    self.move_content_to_folder(other)
                                    self.expand()
                                    self.expected_num_content += 1
                                    other.adjust_color()
                            else: # merge probably cannot merge folder in folders
                                if self.parent == other:
                                    return

                                if other.parent is not None:
                                    if other in other.parent.linked_content:
                                        other.parent.linked_content.remove(other)
                                    other.parent.remove_link(other.parent._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
                                other.delete()

                                for lc in other.linked_content:
                                    lc.remove_link(other._uuid, PySI.LinkingCapability.POSITION, lc._uuid, PySI.LinkingCapability.POSITION)
                                    lc.move(self.x, self.y)
                                    lc.parent = self
                                    lc.parent_level = self.parent_level + 1 if lc.regionname == Folder.regionname else self.parent_level

                                    if lc.regionname != Folder.regionname:
                                        if self.path + "/" + lc.filename in [r.path for r in self.linked_content]:
                                            original_path = lc.path
                                            fn = lc.filename
                                            fp = lc.path

                                            while fn in [r.filename if hasattr(r, "filename") else r.foldername for r in self.linked_content]:
                                                if lc.regionname == FolderIcon.FolderIcon.regionname:
                                                    fn += "_other"
                                                    fp += "_other"
                                                    lc.set_QML_data("name", fp, PySI.DataType.STRING)
                                                else:
                                                    fn = fn[:-4] + "_other" + fn[-4:]
                                                    fp = fp[:-4] + "_other" + fp[-4:]
                                                    lc.set_QML_data("name", fn, PySI.DataType.STRING)

                                            os.rename(original_path, fp)

                                            lc.filename = fn
                                            lc.path = fp
                                    else:
                                        if self.path + "/" + lc.foldername in [r.path for r in self.linked_content]:
                                            original_path = lc.path
                                            while lc.foldername in [r.filename if hasattr(r, "filename") else r.foldername for r in self.linked_content]:
                                                lc.foldername += "_other"
                                                lc.path += "_other"
                                                lc.set_QML_data("name", lc.path, PySI.DataType.STRING)

                                            os.rename(original_path, lc.path)

                                            def rename_folder_content(o):
                                                for l in o.linked_content:
                                                    if l.regionname == Folder.regionname:
                                                        l.path = o.path + "/" + l.foldername
                                                        l.set_QML_data("name", l.path, PySI.DataType.STRING)
                                                        rename_folder_content(l)
                                                    else:
                                                        l.path = o.path + "/" + l.filename

                                                        if l.regionname == FolderIcon.FolderIcon.regionname:
                                                            l.set_QML_data("name", l.path, PySI.DataType.STRING)

                                            rename_folder_content(other)

                                    self.linked_content.append(lc)
                                    self.create_link(self._uuid, PySI.LinkingCapability.POSITION, lc._uuid, PySI.LinkingCapability.POSITION)
                                    self.move_content_to_folder(lc)
                                    self.expand()
                                    self.expected_num_content += 1
                                os.rmdir(other.path)
                        else:
                            if hasattr(other, "is_root"):
                                if other.is_root:
                                    return

                            if self.is_under_user_control:
                                return

                            # from inner folder to outer folder
                            if other.parent is None and other.parent != self and self.parent != other:
                                self.expected_num_content += 1
                                self.move_content_to_folder(other)
                                self.expand()
                            # from outer folder to inner folder
                            elif other.parent is not None and self.parent is not None and other.parent == self.parent:
                                self.expected_num_content += 1
                                self.move_content_to_folder(other)
                                self.expand()
        else:
            if other.was_moved():
                self.color = self.default_color
                self.border_color = self.default_border_color

        if other.is_under_user_control and not self.block_color_change and not self.parent == other:
            folders = [(r, r.parent_level) for r in self.current_regions() if r.regionname == Folder.regionname]
            folders.sort(key=lambda tup: tup[1], reverse=True)
            collisions = [r[0] for r in other.present_collisions() if r[1] == Folder.regionname]

            uid = ""
            for f in folders:
                if f[0]._uuid in collisions:
                    uid = f[0]._uuid
                    break

            if self._uuid == uid:
                if other.enveloped_by(self):
                    self.color = PySI.Color(0, 120, 215, 255)
                    self.border_color = self.default_border_color
                else:
                    self.color = self.default_color
                    self.border_color = PySI.Color(0, 120, 215, 255)

            for f in folders:
                if f[0]._uuid != uid:
                    f[0].color = f[0].default_color
                    f[0].border_color = f[0].default_border_color

    def move_content_to_folder(self, content):
        if not self.is_under_user_control:
            if os.path.commonprefix([self.path, content.path]) != content.path:
                if content.regionname == Folder.regionname:
                    self.__move_content_to_folder__(content, content.foldername, self.path + "/" + content.foldername)
                elif content.regionname == FolderIcon.FolderIcon.regionname:
                    self.__move_content_to_folder__(content, content.filename, self.path + "/" + content.filename)
                else:
                    self.__move_content_to_folder__(content, content.filename, content.filename)

    def __move_content_to_folder__(self, content, fname, fpath):
        if content.path == self.root_path:
            return

        if content.parent is not None:
            content.parent.linked_content.remove(content)
            content.parent.remove_link(content.parent._uuid, PySI.LinkingCapability.POSITION, content._uuid, PySI.LinkingCapability.POSITION)

        content.parent = self

        self.linked_content.append(content)
        self.create_link(self._uuid, PySI.LinkingCapability.POSITION, content._uuid, PySI.LinkingCapability.POSITION)

        os.rename(content.path, self.path + '/' + fname)
        content.path = self.path + '/' + fname
        content.set_QML_data("name", fname, PySI.DataType.STRING)
        self.content = self.__fetch_contents__()

    @SIEffect.on_leave("__PARENT_CONTENT__", SIEffect.EMISSION)
    def on_content_leave_emit(self, other: object) -> None:
        self.color = self.default_color
        self.border_color = self.default_border_color
        if other in self.linked_content and other.is_under_user_control:
            self.linked_content.remove(other)
            self.remove_link(self._uuid, PySI.LinkingCapability.POSITION, other._uuid, PySI.LinkingCapability.POSITION)
            other.parent = None
            self.expected_num_content -= 1
            self.expand()

    def __fetch_contents__(self) -> list:
        return [(entry, FolderIcon if os.path.isdir(entry) else TextFile if entry[entry.rfind("."):] in self.text_file_extensions else ImageFile if entry[entry.rfind("."):] in self.image_file_extensions else TextFile) for entry in glob.glob(self.path + "/*")]

    def num_parents(self):
        if self.parent is None:
            return 0

        s = 0
        parent = self.parent

        while parent is not None:
            s += 1
            parent = parent.parent

        return s

    def sort_content_by_extension(self):
        extensions = {}

        for l in self.linked_content:
            ext = "dir" if (l.regionname == FolderIcon.FolderIcon.regionname or l.regionname == Folder.regionname) else l.filename.split(".")[-1]
            if ext not in extensions:
                extensions[ext] = []
            extensions[ext].append(l)

        return extensions

    def build_delta_movement_contents_list(self, extensions):
        moving_list = []

        extx = 0
        current_height = 0
        ddh = -5
        for ext, la_list in extensions.items():
            grid_width = self.get_grid_width(len(la_list), current_height)
            i = 0
            epy = 0
            dh = ddh
            maxx = 0.0
            for row in range(5):
                epx = extx
                epy += dh + -ddh
                dh = 0
                for col in range(grid_width):
                    if i >= len(la_list):
                        break

                    l = la_list[i]
                    i += 1
                    moving_list.append([l, epx, epy])
                    epx += l.get_region_width() + -ddh
                    if epx > maxx:
                        maxx = epx
                    if dh < l.get_region_height():
                        dh = l.get_region_height()
                    if row + 1 > current_height:
                        current_height = row + 1
            extx = maxx + -ddh

        return moving_list

    def compute_new_aabb(self, moving_list):
        w = 0
        h = 0
        for lc in moving_list:
            if lc[1] + lc[0].width > w:
                w = lc[1] + lc[0].width

            if lc[2] + lc[0].height > h:
                h = lc[2] + lc[0].height

        return w * 0.5, h * 0.5

    def move_content(self, moving_list, centerx, centery, offset_x, offset_y, w, h, enter=False):
        for lc in moving_list:
            lc[0].new_x = lc[1] + centerx - w - lc[0].aabb[0].x
            lc[0].new_y = lc[2] + centery - h - lc[0].aabb[0].y
            lc[0].move(lc[0].new_x, lc[0].new_y)

    def expand(self, toggle=True, offset_x=0.5, offset_y=0.5):
        if self.is_selector:
            return

        self.color = self.default_color
        self.border_color = self.default_border_color

        if len(self.linked_content) == len(self.content):
            moving_list = self.build_delta_movement_contents_list(self.sort_content_by_extension())
            centerx, centery = self.absolute_x_pos() + offset_x * self.get_region_width(), self.absolute_y_pos() + offset_y * self.get_region_height()
            self.move_content(moving_list, centerx, centery, offset_x, offset_y, *self.compute_new_aabb(moving_list))
            self.recalculate_hull()
            self.parent_expand()
            self.is_initial = False
        else: # determine anew if contents are completely present
            if not self.is_initial:
                if len(self.linked_content) == self.expected_num_content:
                    moving_list = self.build_delta_movement_contents_list(self.sort_content_by_extension())
                    centerx, centery = self.absolute_x_pos() + offset_x * self.get_region_width(), self.absolute_y_pos() + offset_y * self.get_region_height()
                    self.move_content(moving_list, centerx, centery, offset_x, offset_y, *self.compute_new_aabb(moving_list))
                    self.emit_linking_action(self._uuid, PySI.LinkingCapability.POSITION, self.position())
                    self.recalculate_hull()
                    self.parent_expand()

    def parent_expand(self):
        if self.parent is not None:
            parent = self.parent
            moving_list = parent.build_delta_movement_contents_list(parent.sort_content_by_extension())
            centerx, centery = parent.absolute_x_pos() + 0.5 * parent.get_region_width(), parent.absolute_y_pos() + 0.5 * parent.get_region_height()
            parent.move_content(moving_list, centerx, centery, 0.5, 0.5, *parent.compute_new_aabb(moving_list))

            for lc in parent.linked_content:
                if lc.regionname == Folder.regionname:
                    lc.emit_linking_action(lc._uuid, PySI.LinkingCapability.POSITION, lc.position())

            parent.recalculate_hull()
            parent.set_QML_data("height", int(parent.aabb[1].y - parent.aabb[0].y), PySI.DataType.INT)
            parent.set_QML_data("widget_width", int(parent.aabb[3].x - parent.aabb[0].x), PySI.DataType.INT)
            ncenterx, ncentery = parent.absolute_x_pos() + 0.5 * parent.get_region_width(), parent.absolute_y_pos() + 0.5 * parent.get_region_height()

            parent.move(parent.x - (ncenterx - centerx), parent.y - (ncentery - centery))
            parent.emit_linking_action(parent._uuid, PySI.LinkingCapability.POSITION, parent.position())

            parent.parent_expand()

    def get_grid_width(self, n, current_height):
        if current_height == 0:
            for i in range(1, 5):
                if i * i >= n:
                    return i
            return 5

        return int(n / current_height + 0.5)

    def recalculate_hull(self) -> None:
        if len(self.linked_content) == 0:
            return

        bboxes_points = []
        for l in self.linked_content:
            temp = [[l.x + l.aabb[i].x, l.y + l.aabb[i].y] for i in range(4)]

            bboxes_points.append([l.absolute_x_pos(), l.absolute_y_pos()])
            bboxes_points.append([l.absolute_x_pos(), l.absolute_y_pos() + l.height])
            bboxes_points.append([l.absolute_x_pos() + l.width, l.absolute_y_pos() + l.height])
            bboxes_points.append([l.absolute_x_pos() + l.width, l.absolute_y_pos()])
            bboxes_points += temp

        self.recalculate_hull_with_additional_points(bboxes_points, False)

    def recalculate_hull_with_additional_points(self, additional_points, needs_shape):
        pts = [[p[0] - self.x, p[1] - self.y] for p in additional_points] + [[p.x - self.x, p.y - self.y] for p in self.shape] if needs_shape else [[p[0] - self.x, p[1] - self.y] for p in additional_points]
        self.shape = PySI.PointVector(self.compute_spline_points([[p.x, p.y] for p in self.explode(self.convex_hull(PySI.PointVector(pts)), 1.05)]))
        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("height", int(self.aabb[1].y - self.aabb[0].y), PySI.DataType.INT)

    def convex_hull(self, points: PySI.PointVector) -> list:
        pts = np.array([[p.x, p.y] for p in points])
        return [PySI.Point3(pts[vert, 0], pts[vert, 1], 1) for vert in ConvexHull(pts).vertices]

    def explode(self, points, factor: float) -> list:
        cx, cy = self.compute_center(points)

        for p in points:
            p.x = cx + (p.x - cx) * factor
            p.y = cy + (p.y - cy) * factor

        return points

    def compute_center(self, points: list) -> tuple:
        return sum([p.x for p in points]) / len(points), sum([p.y for p in points]) / len(points)

    def compute_spline_points(self, points: list) -> list:
        spline = splines.CatmullRom(points, endconditions='closed')
        dots_per_second = 10
        total_duration = spline.grid[-1] - spline.grid[0]
        dots = int(total_duration * dots_per_second) + 1
        times = spline.grid[0] + np.arange(dots) / dots_per_second
        result = spline.evaluate(times).T

        return [[result[0][i], result[1][i]] for i in range(len(result[0]))]

    @SIEffect.on_enter("__HIDE_ENTRY_", SIEffect.RECEPTION)
    def on_hide_entry_enter_recv(self):
        self.remove()
