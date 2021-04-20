from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class ImageEditorBlurToolSetter(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorBlurToolSetter __"
    region_display_name = "ImageEditorBlurToolSetter"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ImageEditorBlurToolSetter, self).__init__(shape, uuid, "", ImageEditorBlurToolSetter.regiontype, ImageEditorBlurToolSetter.regionname, kwargs)

        self.source = "libStdSI"
        self.color = PySI.Color(0, 0, 0, 0)
        self.assigned_uuid = ""
        self.is_active = False

        self.getter = kwargs["getter_segment"] if "getter_segment" in kwargs else None

        if self.getter != None:
            self.getter.setter = self
            self.create_link(self.getter._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.create_link(self.getter._uuid, "PUSH_CONVOLUTION_OUTPUT", self._uuid, "PUSH_CONVOLUTION_OUTPUT")

            for tool in kwargs["other"].image_editor_tool:
                tool.delete()

            kwargs["other"].image_editor_tool = [self, self.getter]

    @SIEffect.on_link(SIEffect.RECEPTION, "PUSH_CONVOLUTION_OUTPUT", "PUSH_CONVOLUTION_OUTPUT")
    def set_conv_output_from_conv_output(self, r, g, b, a):
        self.color = PySI.Color(r, g, b, a)

    @SIEffect.on_continuous("ImageEditorAssign", SIEffect.EMISSION)
    def on_image_editor_tool_assign_continuous_emit(self, other):
        pass

    @SIEffect.on_continuous("ToolApplication", SIEffect.EMISSION)
    def on_tool_apply_continuous_emission(self, other):
        if self.is_active:
            return (self.color.r, self.color.g, self.color.b, self.color.a), "blur_type"

        return None, None

    @SIEffect.on_continuous("ToolActivation", SIEffect.RECEPTION)
    def on_tool_activation_continuous_recv(self, is_active):
        self.is_active = is_active
