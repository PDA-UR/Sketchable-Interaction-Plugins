from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.image_editor.tools.ImageEditorBlurToolSetter import ImageEditorBlurToolSetter


class ImageEditorBlurToolGetter(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorBlurToolGetter __"
    region_display_name = "ImageEditorBlurToolGetter"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ImageEditorBlurToolGetter, self).__init__(shape, uuid, "", ImageEditorBlurToolGetter.regiontype, ImageEditorBlurToolGetter.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = ""
        self.parent_uuid = ""
        self.kwargs = kwargs

        self.link_partner = kwargs["link_partner"] if "link_partner" in kwargs else ""

        self.matrix_size = kwargs["mat_size"] if "mat_size" in kwargs else 3
        self.pixel_size = kwargs["pixel_size"]
        self.color = PySI.Color(55, 55, 55, 255)

        self.required_num_regions = self.matrix_size ** 2

        self.setter = None

        if self.link_partner != "":
            x = kwargs["other_pos"][2] + ((self.matrix_size // 2) * self.pixel_size) - 18 - self.pixel_size // 2
            y = kwargs["other_pos"][3] + ((self.matrix_size // 2) * self.pixel_size) - 24 - self.pixel_size // 2

            self.shape = PySI.PointVector([[x, y], [x, y + self.matrix_size * self.pixel_size], [x + self.matrix_size * self.pixel_size, y + self.matrix_size * self.pixel_size], [x + self.matrix_size * self.pixel_size, y]])
            self.create_link(self.link_partner, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.color = PySI.Color(55, 55, 55, 80)

            self.enable_link_emission("PUSH_CONVOLUTION_OUTPUT", self.push_convolution_output)
            self.enable_link_emission(PySI.LinkingCapability.POSITION, self.position)

            setter_kwargs = {}
            setter_kwargs["pixel_size"] = self.pixel_size
            setter_kwargs["other"] = kwargs["other"]
            setter_kwargs["getter_segment"] = self

            tool_shape = PySI.PointVector([[x + self.pixel_size, y + self.pixel_size], [x + self.pixel_size, y + self.pixel_size * 2], [x + self.pixel_size * 2, y + self.pixel_size * 2], [x + self.pixel_size * 2, y + self.pixel_size]])
            self.create_region_via_name(tool_shape, ImageEditorBlurToolSetter.regionname, kwargs=setter_kwargs)

        self.disable_effect(PySI.CollisionCapability.DELETION, self.RECEPTION)

        self.enable_effect("CONVOLUTION", self.RECEPTION, self.on_convolution_enter_recv, None, self.on_convolution_leave_recv)
        self.enable_effect("IMAGE_PARENT", self.RECEPTION, self.on_parent_enter_recv, None, None)
        self.enable_effect("ImageEditorAssign", self.EMISSION, None, self.on_image_editor_tool_assign_continuous_emit, None)

        self.assigned_uuid = ""
        self.pixels = {}

        self.convoluted_color = (0, 0, 0, 0)

    def on_parent_enter_recv(self, parent_uuid, _):
        if self.parent_uuid == "":
            self.parent_uuid = parent_uuid

            self.create_link(parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.disable_effect("IMAGE_PARENT", self.RECEPTION)

    def on_image_editor_tool_assign_continuous_emit(self, other):
        if self.link_partner == "" and other.left_mouse_active:

            kwargs = self.kwargs
            kwargs["link_partner"] = other._uuid
            kwargs["other_pos"] = other.position()
            kwargs["other"] = other

            self.create_region_via_name(self.shape, ImageEditorBlurToolGetter.regionname, kwargs=kwargs)

    def on_convolution_enter_recv(self, pixel, color):
        if self.link_partner != "":
            if pixel not in self.pixels.keys():
                self.pixels[pixel] = color

            while len(self.pixels) > self.required_num_regions:
                self.pixels.popitem()

            if len(self.pixels) == self.required_num_regions:
                r_conv = 0
                g_conv = 0
                b_conv = 0
                a_conv = 0

                for color in self.pixels.values():
                    r_conv += color.r
                    g_conv += color.g
                    b_conv += color.b
                    a_conv += color.a

                r_conv //= len(self.pixels)
                g_conv //= len(self.pixels)
                b_conv //= len(self.pixels)
                a_conv //= len(self.pixels)

                self.convoluted_color = r_conv, g_conv, b_conv, a_conv

                if self.setter != None:
                    self.emit_linking_action(self._uuid, "PUSH_CONVOLUTION_OUTPUT", self.convoluted_color)

    def on_convolution_leave_recv(self, pixel):
        if self.link_partner != "":
            if pixel in self.pixels.keys():
                del self.pixels[pixel]

    def push_convolution_output(self):
        return self.convoluted_color

    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y