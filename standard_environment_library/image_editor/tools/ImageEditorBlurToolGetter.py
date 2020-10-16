from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.image_editor.tools.ImageEditorBlurToolSetter import ImageEditorBlurToolSetter
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class ImageEditorBlurToolGetter(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorBlurToolGetter __"
    region_display_name = "ImageEditorBlurToolGetter"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        PositionLinkable.__init__(self, shape, uuid, "", ImageEditorBlurToolGetter.regiontype, ImageEditorBlurToolGetter.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, "", ImageEditorBlurToolGetter.regiontype, ImageEditorBlurToolGetter.regionname, kwargs)

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

            setter_kwargs = {}
            setter_kwargs["pixel_size"] = self.pixel_size
            setter_kwargs["other"] = kwargs["other"]
            setter_kwargs["getter_segment"] = self

            tool_shape = PySI.PointVector([[x + self.pixel_size, y + self.pixel_size], [x + self.pixel_size, y + self.pixel_size * 2], [x + self.pixel_size * 2, y + self.pixel_size * 2], [x + self.pixel_size * 2, y + self.pixel_size]])
            self.create_region_via_name(tool_shape, ImageEditorBlurToolSetter.regionname, kwargs=setter_kwargs)

        self.assigned_uuid = ""
        self.pixels = {}

        self.convoluted_color = (0, 0, 0, 0)

    @SIEffect.on_enter("IMAGE_PARENT", SIEffect.RECEPTION)
    def on_parent_enter_recv(self, parent_uuid, _):
        if self.parent_uuid == "":
            self.parent_uuid = parent_uuid

            self.create_link(parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.disable_effect("IMAGE_PARENT", self.RECEPTION)

    @SIEffect.on_continuous("ImageEditorAssign", SIEffect.EMISSION)
    def on_image_editor_tool_assign_continuous_emit(self, other):
        if self.link_partner == "" and other.left_mouse_active:

            kwargs = self.kwargs
            kwargs["link_partner"] = other._uuid
            kwargs["other_pos"] = other.position()
            kwargs["other"] = other

            self.create_region_via_name(self.shape, ImageEditorBlurToolGetter.regionname, kwargs=kwargs)

    @SIEffect.on_enter("CONVOLUTION", SIEffect.RECEPTION)
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

    @SIEffect.on_leave("CONVOLUTION", SIEffect.RECEPTION)
    def on_convolution_leave_recv(self, pixel):
        if self.link_partner != "":
            if pixel in self.pixels.keys():
                del self.pixels[pixel]

    @SIEffect.on_link(SIEffect.EMISSION, "PUSH_CONVOLUTION_OUTPUT")
    def push_convolution_output(self):
        return self.convoluted_color

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y