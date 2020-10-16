from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable


class ImageEditorColorTool(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ImageEditorColorTool __"
    region_display_name = "Color Tool"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        PositionLinkable.__init__(self, shape, uuid, "", ImageEditorColorTool.regiontype, ImageEditorColorTool.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, "", ImageEditorColorTool.regiontype, ImageEditorColorTool.regionname, kwargs)
        self.color = kwargs["color"]
        self.parent_uuid = ""
        self.cursor_id = ""
        self.link_partner = kwargs["link_partner"] if "link_partner" in kwargs else ""
        self.assigned_uuid = ""
        self.kwargs = kwargs

        self.pixel_size = kwargs["pixel_size"]
        self.is_active = False

        if self.link_partner != "":
            x = kwargs["other_pos"][2]
            y = kwargs["other_pos"][3]

            self.shape = PySI.PointVector([[x, y], [x, y + self.pixel_size], [x + self.pixel_size, y + self.pixel_size], [x + self.pixel_size, y]])
            self.create_link(self.link_partner, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

            for tool in kwargs["other"].image_editor_tool:
                tool.delete()

            kwargs["other"].image_editor_tool = [self]

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

            self.create_region_via_name(self.shape, ImageEditorColorTool.regionname, kwargs=kwargs)

    @SIEffect.on_continuous("ToolActivation", SIEffect.RECEPTION)
    def on_tool_activation_continuous_recv(self, is_active):
            self.is_active = is_active

    @SIEffect.on_continuous("ToolApplication", SIEffect.EMISSION)
    def on_tool_apply_continuous_emission(self, other):
        if self.is_active:
            return (self.color.r, self.color.g, self.color.b, self.color.a), "color_type"

        return None, None