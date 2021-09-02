from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Terminal(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.terminal_name
    region_display_name = E.id.terminal_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Terminal, self).__init__(shape, uuid, E.id.terminal_texture, Terminal.regiontype, Terminal.regionname, kwargs)

        self.qml_path = self.set_QML_path(E.id.terminal_qml_file_name)
        self.color = E.color.terminal_color
        self.letter_color = E.id.terminal_letter_color

        self.shape = self.aabb
        self.message_header = "Showing messages of SI plugins:\n"

        self.set_QML_data("width", self.width, PySI.DataType.INT)
        self.set_QML_data("height", self.height, PySI.DataType.INT)

    @SIEffect.on_enter(E.capability.canvas_logging, SIEffect.RECEPTION)
    def on_logging_enter_recv(self):
        self.set_QML_data("visible", False, PySI.DataType.BOOL)
        self.set_QML_data("message", self.message_header, PySI.DataType.STRING)

    @SIEffect.on_continuous(E.capability.canvas_logging, SIEffect.RECEPTION)
    def on_logging_continuous_recv(self, log, update):
        if update:
            self.set_QML_data("message", log, PySI.DataType.STRING)
