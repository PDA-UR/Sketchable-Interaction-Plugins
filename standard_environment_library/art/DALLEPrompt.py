from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class DALLEPrompt(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ DALLEPrompt __"
    region_display_name = "DALLEPrompt"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(DALLEPrompt, self).__init__(shape, uuid, "res/prompt.png", DALLEPrompt.regiontype, DALLEPrompt.regionname, kwargs)
        self.qml_path = self.set_QML_path("DALLEPrompt.qml")
        self.color = PySI.Color(255, 255, 0, 255)
        self.prompt = ""

    @SIEffect.on_enter("__ON_DALLE_PROMPT__", SIEffect.EMISSION)
    def on_dalle_prompt_enter(self, other):
        self.prompt = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)

        return self.prompt

    @SIEffect.on_leave("__ON_DALLE_PROMPT__", SIEffect.EMISSION)
    def on_dalle_prompt_enter(self, other):
        self.prompt = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)

        return self.prompt
