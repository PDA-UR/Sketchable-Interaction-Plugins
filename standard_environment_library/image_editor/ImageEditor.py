from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.image_editor.pixel.ImageEditorPixel import ImageEditorPixel
from plugins.standard_environment_library.image_editor.tools.ImageEditorColorTool import ImageEditorColorTool
from plugins.standard_environment_library.image_editor.tools.ImageEditorBlurToolGetter import ImageEditorBlurToolGetter
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

from plugins.E import E

from PIL import Image


class ImageEditor(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.image_editor_name
    region_display_name = E.id.image_editor_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        Deletable.__init__(self, shape, uuid, E.id.image_editor_texture, ImageEditor.regiontype, ImageEditor.regionname, kwargs)
        Movable.__init__(self, shape, uuid, E.id.image_editor_texture, ImageEditor.regiontype, ImageEditor.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, E.id.image_editor_texture, ImageEditor.regiontype, ImageEditor.regionname, kwargs)

        self.qml_path = self.set_QML_path(E.id.image_editor_qml_file_path)
        self.color = E.id.image_editor_color
        self.text_height = E.id.image_editor_text_height

        self.img = None
        self.children = []
        self.image_target_file_path = ""

        self.pixel_size = E.id.image_editor_pixel_size
        self.offset = E.id.image_editor_offset
        self.border = E.id.image_editor_border
        self.pixels = []

    @SIEffect.on_enter(E.id.image_editor_capability_image_parent, SIEffect.EMISSION)
    def on_parent_enter_emit(self, other):
        if other.regionname == ImageEditorPixel.regionname:
            self.children[other.index] = other
            color = list(self.pixels[other.index]) + [E.id.image_editor_max_color_value]
            return self._uuid, color

        self.children.append(other)

        return self._uuid, 0

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        for child in self.children:
            child.delete()

        self.children = []

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_continuous(E.id.image_editor_capability_grab_image, SIEffect.EMISSION)
    def on_grab_image_continuous_emit(self, other):
        if other.path != "" and self.image_target_file_path != other.path and not other.is_under_user_control:
            self.image_target_file_path = other.path
            self.img = Image.open(other.path)
            self.img_width, self.img_height = self.img.size
            self.pixels = list(self.img.getdata())
            self.children = [None] * len(self.pixels)

            self.color = E.id.image_editor_color

            x = self.relative_x_pos()
            y = self.relative_y_pos()
    
            tool_width = E.id.image_editor_tool_width
            tool_height = E.id.image_editor_tool_height

            self.width = (self.pixel_size + self.offset) * self.img_width + self.border * 3 + tool_width
            self.height = (self.pixel_size + self.offset) * self.img_height + self.border * 4 + self.text_height
            self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])
    
            tool_kwargs = {}
            tool_kwargs["color"] = E.id.image_editor_color_red
            tool_kwargs["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border + self.text_height], [x + self.border, y + tool_height + self.border + self.text_height], [x + tool_width + self.border, y + tool_height + self.border + self.text_height], [x + tool_width + self.border, y + self.border + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorColorTool.regionname, kwargs=tool_kwargs)

            tool_kwargs2 = {}
            tool_kwargs2["color"] = E.id.image_editor_color_green
            tool_kwargs2["pixel_size"] = self.pixel_size
            tool_shape = PySI.PointVector([[x + self.border, y + self.border * 2 + tool_height + self.text_height], [x + self.border, y + tool_height + self.border * 2 + tool_height + self.text_height], [x + tool_width + self.border, y + tool_height + self.border * 2 + tool_height + self.text_height], [x + tool_width + self.border, y + self.border * 2 + tool_height + self.text_height]])
            self.create_region_via_name(tool_shape, ImageEditorColorTool.regionname, kwargs=tool_kwargs2)

            tool_kwargs3 = {}
            tool_kwargs3["color"] = E.id.image_editor_color_blue
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

    @SIEffect.on_leave(E.id.image_editor_capability_grab_image, SIEffect.EMISSION)
    def on_grab_image_leave_emit(self, other):
        pixels = []

        for child in self.children:
            if child.regionname == ImageEditorPixel.regionname:
                pixels.append((int(child.color.r), int(child.color.g), int(child.color.b)))

            child.delete()

        self.img.putdata(pixels)
        self.img.save(self.image_target_file_path)
        self.color = E.id.image_editor_color
        self.set_QML_data("img_path", self.texture_path, PySI.DataType.STRING)
        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
        self.image_target_file_path = ""
        self.children = []

        self.set_QML_data("name", "", PySI.DataType.STRING)

    @SIEffect.on_leave(E.id.image_editor_capability_hide_tool, SIEffect.EMISSION)
    def on_hide_tool_leave_emit(self, other):
        pass