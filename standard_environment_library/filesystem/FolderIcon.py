from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem import Folder
from plugins.standard_environment_library.filesystem.Content import Content

from plugins.E import E
import glob
import os


class FolderIcon(Content):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ FolderIcon __"
    region_display_name = "FolderIcon"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super().__init__(shape, uuid, "res/dir.png", FolderIcon.regiontype, FolderIcon.regionname, kwargs)
        self.qml_path = self.set_QML_path("FolderIcon.qml")
        self.path = "" if "path" not in kwargs else kwargs["path"]
        self.filename = "" if self.path == "" else self.path[self.path.rfind("/") + 1:]

        name = self.adjust_path_for_duplicate_numbered() if self.path == "" else self.filename

        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)
        self.set_QML_data("color", self.text_color, PySI.DataType.STRING)
        self.set_QML_data("name", name, PySI.DataType.STRING)

    def adjust_path_for_duplicate_numbered(self):
        self.path = self.root_path + "/.temp"
        n = "untitled_folder"
        i = sum(element[index:index + len(n)] == n for element in [r.foldername for r in self.current_regions() if r.regionname == Folder.Folder.regionname] + [r.filename for r in self.current_regions() if r.regionname == FolderIcon.regionname] for index, char in enumerate(element))
        self.filename = n if i == 0 else n + f"{i+1}"
        self.path += "/" + self.filename
        name = self.filename

        try:
            os.mkdir(self.path)
        except:
            pass

        return name

    def adjust_for_duplicate_other(self, other):
        content = [entry for entry in glob.glob(self.path + "/*")]
        fn = other.filename if other.regionname != Folder.Folder.regionname else other.foldername
        fp = other.path
        original_path = other.path

        while self.path + "/" + fn in content:
            if other.regionname == FolderIcon.regionname or other.regionname == Folder.Folder.regionname:
                fn += "_other"
                fp += "_other"
                other.set_QML_data("name", fp, PySI.DataType.STRING)
            else:
                fn = fn[:-4] + "_other" + fn[-4:]
                fp = fp[:-4] + "_other" + fp[-4:]
                other.set_QML_data("name", fn, PySI.DataType.STRING)
        os.rename(original_path, fp)

        return fn, fp

    def show_highlight(self, other):
        if other.parent is not None:
            other.parent.block_color_change = True
            other.parent.color = other.parent.default_color
            other.parent.border_color = other.parent.default_border_color
        else:
            folders = [(r, r.parent_level) for r in self.current_regions() if r.regionname == Folder.Folder.regionname]
            for f in folders:
                f[0].color = f[0].default_color
                f[0].border_color = f[0].default_border_color
                f[0].block_color_change = True

        self.set_QML_data("is_highlighted", True, PySI.DataType.BOOL)

    def hide_highlight(self, other):
        self.set_QML_data("is_highlighted", False, PySI.DataType.BOOL)
        if other.parent is not None:
            other.parent.block_color_change = False
        else:
            folders = [(r, r.parent_level) for r in self.current_regions() if r.regionname == Folder.Folder.regionname]
            for f in folders:
                f[0].color = f[0].default_color
                f[0].border_color = f[0].default_border_color
                f[0].block_color_change = False

    def toggle_highlight(self, other, toggle):
        if toggle:
            self.show_highlight(other)
        else:
            self.hide_highlight(other)

    @SIEffect.on_continuous("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_continuous_recv(self, canvas_uuid: str) -> None:
        super().on_canvas_continuous_recv(canvas_uuid)
        self.rename()

    @SIEffect.on_continuous("__PARENT_CONTENT_ICON__", SIEffect.EMISSION)
    def on_content_enter_continuous(self, other):
        if other.was_moved():
            if self.parent != other:
                fn, fp = self.adjust_for_duplicate_other(other)
                if other.regionname != Folder.Folder.regionname:
                    other.filename = fn
                else:
                    other.foldername = fn

                other.path = fp
                self.move_content_to_folder(other)
                self.set_QML_data("is_highlighted", False, PySI.DataType.BOOL)
        else:
            if other.is_under_user_control and self.parent != other:
                self.toggle_highlight(other, True)

    def move_content_to_folder(self, content):
        if not self.is_under_user_control:
            if os.path.commonprefix([self.path, content.path]) != content.path:
                if content.regionname == Folder.Folder.regionname:
                    self.__move_content_to_folder__(content, content.foldername, self.path + "/" + content.foldername)
                    content.remove()
                elif content.regionname == FolderIcon.regionname:
                    self.__move_content_to_folder__(content, content.filename, self.path + "/" + content.filename)
                else:
                    self.__move_content_to_folder__(content, content.filename, self.path + "/" + content.filename)

    def __move_content_to_folder__(self, content, fname, fpath):
        if content.path == self.root_path:
            return

        if content.parent is not None:
            content.parent.remove_content_and_link(content)
        content.is_removed = True
        content.delete()

        os.rename(content.path, fpath)

    @SIEffect.on_leave("__PARENT_CONTENT_ICON__", SIEffect.EMISSION)
    def on_content_enter_leave(self, other):
        if other.is_under_user_control and self.parent != other:
            if other.is_under_user_control and self.parent != other:
                self.toggle_highlight(other, False)

    def on_double_clicked(self):
        self.morph()

    def compute_morph_coordinates(self):
        if self.parent is not None:
            if self in self.parent.linked_content:
                self.parent.linked_content.remove(self)
            self.parent.remove_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.is_removed = True
            centerx, centery = self.parent.aabb[0].x + (self.parent.aabb[3].x - self.parent.aabb[0].x) / 2, self.parent.aabb[0].y + (self.parent.aabb[1].y - self.parent.aabb[0].y) / 2
            x = centerx - self.icon_width / 2 + self.parent.x
            y = centery - self.icon_height / 2 + self.parent.y
        else:
            centerx, centery = self.aabb[0].x + (self.aabb[3].x - self.aabb[0].x) / 2, self.aabb[0].y + (self.aabb[1].y - self.aabb[0].y) / 2
            x = centerx - self.icon_width / 2
            y = centery - self.icon_height / 2

        return x, y

    def morph(self):
        x, y = self.compute_morph_coordinates()
        kwargs = {}
        kwargs["parent"] = self.parent if self.parent is not None else None
        kwargs["path"] = self.path
        kwargs["morphed"] = True if self.parent is not None else False
        self.delete()
        self.create_region_via_class([[x, y], [x, y + self.icon_height], [x + self.icon_width, y + self.icon_height], [x + self.icon_width, y]], Folder, kwargs)