from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect


class ImageEditorBlurToolSetter(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorBlurToolSetter __"
    region_display_name = "ImageEditorBlurToolSetter"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ImageEditorBlurToolSetter, self).__init__(shape, uuid, "", ImageEditorBlurToolSetter.regiontype, ImageEditorBlurToolSetter.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = ""
        self.color = PySI.Color(0, 0, 0, 0)
        self.disable_effect(PySI.CollisionCapability.DELETION, self.RECEPTION)
        self.assigned_uuid = ""
        self.is_active = False

        self.enable_effect("ToolActivation", self.RECEPTION, None, self.on_tool_activation_continuous_recv, None)
        self.enable_effect("ToolApplication", self.EMISSION, None, self.on_tool_apply_continuous_emission, None)
        self.enable_effect("ImageEditorAssign", self.EMISSION, None, self.on_image_editor_tool_assign_continuous_emit, None)
        self.enable_link_reception("PUSH_CONVOLUTION_OUTPUT", "PUSH_CONVOLUTION_OUTPUT", self.set_conv_output_from_conv_output)

        self.getter = kwargs["getter_segment"] if "getter_segment" in kwargs else None

        if self.getter != None:
            self.getter.setter = self
            self.create_link(self.getter._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.create_link(self.getter._uuid, "PUSH_CONVOLUTION_OUTPUT", self._uuid, "PUSH_CONVOLUTION_OUTPUT")

            for tool in kwargs["other"].image_editor_tool:
                tool.delete()

            kwargs["other"].image_editor_tool = [self, self.getter]

    def set_conv_output_from_conv_output(self, r, g, b, a):
        self.color = PySI.Color(r, g, b, a)

    def on_image_editor_tool_assign_continuous_emit(self, other):
        pass

    def on_tool_apply_continuous_emission(self, other):
        if self.is_active:
            return (self.color.r, self.color.g, self.color.b, self.color.a), "blur_type"

        return None, None

    def on_tool_activation_continuous_recv(self, is_active):
        self.is_active = is_active
