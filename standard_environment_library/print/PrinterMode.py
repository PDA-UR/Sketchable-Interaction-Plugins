from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class PrinterMode(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.printer_mode_regionname
    region_display_name = E.id.printer_mode_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(PrinterMode, self).__init__(shape, uuid, "", PrinterMode.regiontype, PrinterMode.regionname, kwargs)
        self.parent_uuid = kwargs["parent"]
        self.mode = kwargs["mode"]
        self.qml_path = self.set_QML_path(E.id.printer_mode_qml_path)

        self.set_QML_data("text", self.mode, PySI.DataType.STRING)

    @SIEffect.on_enter(E.capability.print_printer_mode_selected, SIEffect.EMISSION)
    def on_printer_mode_selected_enter_emit(self, other: object) -> str:
        return self.mode

    @SIEffect.on_leave(E.capability.print_printer_mode_selected, SIEffect.EMISSION)
    def on_printer_mode_selected_leave_emit(self, other: object) -> None:
        pass

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        self.create_link(self.parent_uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
