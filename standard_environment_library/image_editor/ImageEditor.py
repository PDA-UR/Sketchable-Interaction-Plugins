from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.image_editor.pixel.ImageEditorPixel import ImageEditorPixel
from plugins.standard_environment_library.image_editor.tools.ImageEditorColorTool import ImageEditorColorTool
from plugins.standard_environment_library.image_editor.tools.ImageEditorBlurToolGetter import ImageEditorBlurToolGetter

from PIL import Image


class ImageEditor(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ ImageEditor __"
    region_display_name = "Edit Image"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ImageEditor, self).__init__(shape, uuid, "res/editor_icon.png", ImageEditor.regiontype, ImageEditor.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("ImageEditor.qml")

        self.color = PySI.Color(255, 229, 204, 255)

        self.text_height = 50

        self.enable_effect("HIDE_TOOL", self.EMISSION, None, None, self.on_hide_tool_leave_emit)
        self.enable_effect("GRAB_IMAGE", self.EMISSION, None, self.on_grab_image_continuous_emit, self.on_grab_image_leave_emit)
        self.enable_effect("IMAGE_PARENT", self.EMISSION, self.on_parent_enter_emit, None, None)
        self.enable_effect(PySI.CollisionCapability.DELETION, self.RECEPTION, self.on_deletion_enter_recv, None, None)
        self.enable_link_emission(PySI.LinkingCapability.POSITION, self.position)
        self.img = None
        self.children = []
        self.image_target_file_path = ""

        self.pixel_size = 10
        self.offset = 1
        self.border = 15
        self.pixels = []

    def on_parent_enter_emit(self, other):

        if other.regionname == ImageEditorPixel.regionname:
            self.children[other.index] = other
            color = list(self.pixels[other.index]) + [255]
            return self._uuid, color

        self.children.append(other)

        return self._uuid, 0

    def on_deletion_enter_recv(self):
        for child in self.children:
            child.delete()

        self.children = []

    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    def on_grab_image_continuous_emit(self, other):
        if other.path != "" and self.image_target_file_path != other.path and not other.is_under_user_control:
            self.image_target_file_path = other.path
            self.img = Image.open(other.path)
            self.img_width, self.img_height = self.img.size
            self.pixels = list(self.img.getdata())
            self.children = [None] * len(self.pixels)

            self.color = PySI.Color(255, 229, 204, 255)

            x = self.relative_x_pos()
            y = self.relative_y_pos()
    
            tool_width = 50
            tool_height = 50

            self.width = (self.pixel_size + self.offset) * self.img_width + self.border * 3 + tool_width
            self.height = (self.pixel_size + self.offset) * self.img_height + self.border * 4 + self.text_height
            self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])
    
            tool_kwargs = {}
            tool_kwargs["color"] = PySI.Color(255, 0, 0, 255)
            tool_kwargs["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border + self.text_height], [x + self.border, y + tool_height + self.border + self.text_height], [x + tool_width + self.border, y + tool_height + self.border + self.text_height], [x + tool_width + self.border, y + self.border + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorColorTool.regionname, kwargs=tool_kwargs)

            tool_kwargs2 = {}
            tool_kwargs2["color"] = PySI.Color(0, 255, 0, 255)
            tool_kwargs2["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border * 2 + tool_height + self.text_height], [x + self.border, y + tool_height + self.border * 2 + tool_height + self.text_height], [x + tool_width + self.border, y + tool_height + self.border * 2 + tool_height + self.text_height], [x + tool_width + self.border, y + self.border * 2 + tool_height + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorColorTool.regionname, kwargs=tool_kwargs2)

            tool_kwargs3 = {}
            tool_kwargs3["color"] = PySI.Color(0, 0, 255, 255)
            tool_kwargs3["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border * 3 + tool_height * 2 + self.text_height], [x + self.border, y + tool_height * 2+ self.border * 3 + tool_height + self.text_height], [x + tool_width + self.border, y + tool_height * 2 + self.border * 3 + tool_height + self.text_height], [x + tool_width + self.border, y + self.border * 3 + tool_height * 2 + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorColorTool.regionname, kwargs=tool_kwargs3)

            tool_kwargs4 = {}
            tool_kwargs4["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border * 4 + tool_height * 3 + self.text_height], [x + self.border, y + tool_height * 3 + self.border * 4 + tool_height + self.text_height], [x + tool_width + self.border, y + tool_height * 3 + self.border * 4 + tool_height + self.text_height], [x + tool_width + self.border, y + self.border * 4 + tool_height * 3 + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorBlurToolGetter.regionname, kwargs=tool_kwargs4)

            start_x = x + self.border + tool_width + self.offset + self.border
            start_y = y + self.border + self.text_height
    
            current_x = start_x
            current_y = start_y
    
            for i in range(self.img_height):
                for k in range(self.img_width):
                    shape = [[current_x, current_y], [current_x, current_y + self.pixel_size], [current_x + self.pixel_size, current_y + self.pixel_size], [current_x + self.pixel_size, current_y]]
                    self.create_region_via_name(shape, ImageEditorPixel.regionname, False, {"index": self.img_height * k + i})

                    current_y += self.offset + self.pixel_size
    
                current_x += self.offset + self.pixel_size
                current_y = start_y

            self.set_QML_data("img_path", "", PySI.DataType.STRING)
            self.set_QML_data("name", other.filename, PySI.DataType.STRING)
            self.set_QML_data("container_width", self.width, PySI.DataType.INT)
            self.set_QML_data("container_height", self.height, PySI.DataType.INT)

    def on_grab_image_leave_emit(self, other):
        pixels = []

        for child in self.children:
            if child.regionname == ImageEditorPixel.regionname:
                pixels.append((int(child.color.r), int(child.color.g), int(child.color.b)))

            child.delete()

        self.img.putdata(pixels)
        self.img.save(self.image_target_file_path)
        self.color = PySI.Color(225, 225, 225, 255)
        self.set_QML_data("img_path", self.texture_path, PySI.DataType.STRING)
        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
        self.image_target_file_path = ""
        self.children = []

        self.set_QML_data("name", "", PySI.DataType.STRING)

    def on_hide_tool_leave_emit(self, other):
        pass