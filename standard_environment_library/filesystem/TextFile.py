from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.filesystem.File import File
from plugins.standard_environment_library.filesystem import InteractionPriorization
from plugins.E import E
import os


class TextFile(File):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ TextFile __"
    region_display_name = "TextFile"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TextFile, self).__init__(shape, uuid, "res/file_icon.png", TextFile.regiontype, TextFile.regionname, kwargs)
        cw, ch = self.context_dimensions()
        self.qml_path = self.set_QML_path("TextFile.qml")
        self.edit_width = cw / 5
        self.edit_height = int(self.edit_width * 29.7 / 21)
        self.is_in_icon_view = True
        self.is_in_edit_view = False
        self.text = ""
        self.border_width = 2
        self.is_text: SIEffect.SI_CONDITION = True

        if self.path != "":
            try:
                f = open(self.path, "r")
                text = f.read()
                f.close()
                self.text = text
                self.set_QML_data("content", self.text, PySI.DataType.STRING)
            except:
                pass

        is_drawn = True if "DRAWN" in kwargs and kwargs["DRAWN"] else False

        if self.path == "" and is_drawn:
            self.path = self.desktop_path + "/new_file.txt"
            self.path = self.handle_duplicate_renaming(self.path)
            self.entryname = self.path[self.path.rfind("/") + 1:]

            open(self.path, 'w').close()

            self.set_QML_data("name", self.entryname, PySI.DataType.STRING)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("edit_view", self.is_in_edit_view, PySI.DataType.BOOL)

    def handle_duplicate_renaming(self, path):
        while os.path.exists(path):
            path = path[:path.rfind(f".txt")] + "_other" + f".txt"

        return path

    @SIEffect.on_continuous("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_continuous_recv(self):
        return
        self.set_QML_data("is_overlay_visible", False, PySI.DataType.BOOL)

    @SIEffect.on_leave("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_leave_recv(self):
        return
        self.set_QML_data("is_overlay_visible", True, PySI.DataType.BOOL)

    def to_edit_view(self):
        self.with_border = True
        self.is_in_icon_view = False
        self.is_in_edit_view = True

        self.color = PySI.Color(230, 230, 230, 255)
        self.width = int(self.edit_width)
        self.height = int(self.edit_height)
        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]
                                       ])

        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("edit_view", self.is_in_edit_view, PySI.DataType.BOOL)
        self.set_QML_data("widget_width", self.width, PySI.DataType.INT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.INT)

    def to_icon(self):
        self.color = PySI.Color(230, 230, 230, 0)
        self.with_border = False
        self.is_in_icon_view = True
        self.is_in_edit_view = False

        self.width = self.icon_width * 2
        self.height = self.icon_height + self.text_height
        self.shape = PySI.PointVector([[self.aabb[0].x, self.aabb[0].y],
                                       [self.aabb[0].x, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y + self.height],
                                       [self.aabb[0].x + self.width, self.aabb[0].y]
                                       ])

        self.set_QML_data("widget_width", self.width, PySI.DataType.INT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.INT)
        self.set_QML_data("icon_view", self.is_in_icon_view, PySI.DataType.BOOL)
        self.set_QML_data("edit_view", self.is_in_edit_view, PySI.DataType.BOOL)
        self.set_QML_data("icon_width", self.icon_width, PySI.DataType.INT)
        self.set_QML_data("icon_height", self.icon_height, PySI.DataType.INT)

    def on_double_clicked(self):
        if self.parent is None:
            if self.is_in_icon_view:
                self.to_edit_view()
            else:
                self.to_icon()
                new_content = self.get_QML_data("te_content", PySI.DataType.STRING)
                if new_content == "":
                    return

                self.text = new_content
                self.set_QML_data("content", self.text, PySI.DataType.STRING)

                if self.path != "":
                    f = open(self.path, "w")
                    f.write(new_content)
                    f.close()
            return True

        return False

    @SIEffect.on_enter("__ON_DALLE_PROMPT__", SIEffect.EMISSION)
    def on_dalle_prompt_enter(self, other):
        lines = []
        with open(self.path, "r") as f:
            lines = f.readlines()

        self.prompt = " ".join(lines)
        print(self.prompt)

        return self.prompt

    @SIEffect.on_leave("__ON_DALLE_PROMPT__", SIEffect.EMISSION)
    def on_dalle_prompt_leave(self, other):
        lines = []
        with open(self.path, "r") as f:
            lines = f.readlines()

        self.prompt = " ".join(lines)
        print(self.prompt)

        return self.prompt

