from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class ImageEditorPixel(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorPixel __"
    region_display_name = "ImageEditorPixel"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        PositionLinkable.__init__(self, shape, uuid, "", ImageEditorPixel.regiontype, ImageEditorPixel.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, "", ImageEditorPixel.regiontype, ImageEditorPixel.regionname, kwargs)

        self.parent_uuid = ""
        self.index = kwargs["index"]

        r, g, b, a = kwargs["color"] if "color" in kwargs else (255, 255, 255, 255)
        self.color = PySI.Color(r, g, b, a)

    @SIEffect.on_enter("IMAGE_PARENT", SIEffect.RECEPTION)
    def on_parent_enter_recv(self, parent_uuid, target_color):
        if self.parent_uuid == "":
            self.parent_uuid = parent_uuid
            self.create_link(parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
            self.disable_effect("IMAGE_PARENT", self.RECEPTION)

            r, g, b, a = target_color
            self.color = PySI.Color(r, g, b, a)

    @SIEffect.on_continuous("ToolApplication", SIEffect.RECEPTION)
    def on_tool_apply_continuous_recv(self, tool, tooltype):
        if tool != None and tooltype != None:
            if self.color != tool:
                self.color = PySI.Color(tool[0], tool[1], tool[2], tool[3])

    @SIEffect.on_enter("CONVOLUTION", SIEffect.EMISSION)
    def on_convolution_enter_emit(self, other):
        return self._uuid, self.color

    @SIEffect.on_leave("CONVOLUTION", SIEffect.EMISSION)
    def on_convolution_leave_emit(self, other):
        return self._uuid