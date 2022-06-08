from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class CBSplitterConditionalVariable(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ CBSplitterConditionalVariable __"
    region_display_name = "CBSplitterConditionalVariable"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(CBSplitterConditionalVariable, self).__init__(shape, uuid, "", CBSplitterConditionalVariable.regiontype, CBSplitterConditionalVariable.regionname, kwargs)
        self.qml_path = self.set_QML_path("CBSplitterConditionalVariable.qml")
        self.color = PySI.Color(255, 0, 0, 255)
        self.with_border = True
        self.border_width = 2
        self.parent = kwargs["parent"]
        self.variable_identifier = kwargs["identifier"]
        self.parent.cond_vars.append(self)
        self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.set_QML_data("text", self.variable_identifier, PySI.DataType.STRING)
        self.no_entry_image = "res/no_entry.png"

        if self.variable_identifier == "is_text":
            self.icon = "../filesystem/res/file_icon.png"
        elif self.variable_identifier == "image":
            self.icon = "../filesystem/res/image.png"
        elif self.variable_identifier == "is_folder":
            self.icon = "../filesystem/res/dir.png"
        else:
            self.icon = "../email/res/email.png"

        self.set_QML_data("variable_image", self.icon, PySI.DataType.STRING)

    @SIEffect.on_enter("__CONDITIONAL_VARIABLE_ADD__", SIEffect.EMISSION)
    def on_conditional_variable_add_enter_emit(self, other):
        return self.variable_identifier, self.icon

    @SIEffect.on_leave("__CONDITIONAL_VARIABLE_ADD__", SIEffect.EMISSION)
    def on_conditional_variable_add_leave_emit(self, other):
        return self.variable_identifier, self.icon