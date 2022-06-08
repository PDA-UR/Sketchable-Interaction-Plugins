from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library.filesystem.FolderBubble import FolderBubble
from plugins.standard_environment_library.filesystem.FilesystemAccess import FilesystemAccess
import os
import splines
import numpy as np

class FolderSplit(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ FolderSplit __"
    region_display_name = "FolderSplit"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FolderSplit, self).__init__(shape, uuid, "res/split.png", FolderSplit.regiontype, FolderSplit.regionname, kwargs)
        self.qml_path = self.set_QML_path("FolderSplit.qml")
        self.color = PySI.Color(255, 0, 0, 255)
        self.has_split = False
        cw, ch = self.context_dimensions()
        self.icon_width = cw // 39
        self.icon_height = ch // 17
        self.text_height = ch // 22
        self.entry_spacing_offset = cw / 384

        self.split_offset = 100 / 1920 * cw

    def grid_dimensions(self, n, max_cols=5):
        rows = int(n / max_cols) + 1 if n % max_cols != 0 else int(n / max_cols)
        rows = rows if rows != 0 else 1
        cols = n / rows
        return rows, int(cols) if cols.is_integer() else int(cols) + 1

    def build_movement_list(self, shape, offset, lc):
        rows, cols = self.grid_dimensions(len(lc))
        moves = []
        y = min(shape, key=lambda x: x[1])[1]
        ty = 0
        for row in range(rows):
            x = min(shape, key=lambda x: x[0])[0]
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

    def compute_center(self, points):
        return sum([p[0] for p in points]) / len(points), sum([p[1] for p in points]) / len(points)

    def explode(self, points, factor):
        cx, cy = self.compute_center(points)

        for p in points:
            p[0] = cx + (p[0] - cx) * factor
            p[1] = cy + (p[1] - cy) * factor

        return points

    def splines(self, pts):
        spline = splines.CatmullRom(pts, endconditions='closed')
        dots_per_second = 10
        total_duration = spline.grid[-1] - spline.grid[0]
        dots = int(total_duration * dots_per_second) + 1
        times = spline.grid[0] + np.arange(dots) / dots_per_second
        result = spline.evaluate(times).T

        return [[result[0][i], result[1][i]] for i in range(len(result[0]))]

    @SIEffect.on_enter("__FOLDER_SPLIT__", SIEffect.EMISSION)
    def on_folder_split_enter_emit(self, other):
        if not self.has_split:
            split_target = self.entries_parent()
            split_entries = self.split_entries(split_target._uuid)
            path = split_target.path[:split_target.path.rfind("/")] + "/" + split_target.entryname + "_other"
            if not os.path.exists(path):
                os.mkdir(path)

            if len(split_entries) > 0:
                for e in split_entries:
                    split_target.linked_content.remove(e)
                    e.remove_link(split_target._uuid, PySI.LinkingCapability.POSITION, e._uuid, PySI.LinkingCapability.POSITION)
                    os.rename(e.path, path + "/" + e.entryname)
                    e.parent = None
                    e.is_ready = False
                    e.remove()

                split_target.expand()

                x, y = split_target.absolute_x_pos() + split_target.width + self.split_offset, split_target.absolute_y_pos()
                shape = [[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]]

                _, grid_pts = self.build_movement_list(shape, self.entry_spacing_offset, split_entries)
                exploded = self.explode(grid_pts, 1.05)
                shape = self.splines(exploded)

                self.create_region_via_name(shape, FolderBubble.regionname, False, {"parent": split_target.parent, "path": path, "open": False, "hierarchy_level": 0, "root": False, "root_path": FilesystemAccess.root_path, "is_split": True})

            self.has_split = True
            self.delete()

    def entries_parent(self):
        folders = sorted([r for r in self.current_regions() if r._uuid in [e[0] for e in self.present_collisions() if e[1] == "__ FolderBubble __"]], key=lambda x: x.parent_level)
        return folders[0] if len(folders) > 0 else None

    def split_entries(self, parent_uuid):
        return [r for r in self.current_regions() if hasattr(r, "parent") and r.parent is not None and r.parent._uuid == parent_uuid and r._uuid in [e[0] for e in self.present_collisions()]]