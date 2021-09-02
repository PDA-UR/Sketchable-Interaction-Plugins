from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.print.Printer import Printer
from plugins.standard_environment_library.print.PrinterMode import PrinterMode

from plugins.E import E

import os, time, pyautogui
from subprocess import Popen, PIPE


class Print(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.print_regionname
    region_display_name = E.id.print_region_display_name

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Print, self).__init__(shape, uuid, E.id.print_texture, Print.regiontype, Print.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.print_qml_path)
        self.available_printers = [printer.decode().strip() for printer in Popen(E.id.print_linux_command_fetch_printer_names, stdout=PIPE, shell=True).stdout.readlines()]
        self.selected_printer = None
        self.selected_print_mode = None
        self.printer_region_width = 125
        self.printer_region_height = 50
        self.printer_mode_region_width = 100
        self.printer_mode_region_height = 50
        self.offset = 5
        self.PRINTER_MODE_DIALOG = E.id.print_dialog

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        for printer_name in self.available_printers:
            x, y = self.aabb[3].x + self.offset, self.aabb[3].y
            shape = [[x, y], [x, y + self.printer_region_height], [x + self.printer_region_width, y + self.printer_region_height], [x + self.printer_region_width, y]]
            self.create_region_via_name(shape, Printer.regionname, kwargs={"parent": self._uuid, "name": printer_name})

        x, y = self.aabb[0].x - self.offset - self.printer_mode_region_width, self.aabb[0].y

        shape = [[x, y], [x, y + self.printer_mode_region_height], [x + self.printer_mode_region_width, y + self.printer_mode_region_height], [x + self.printer_mode_region_width, y]]
        self.create_region_via_name(shape, PrinterMode.regionname, kwargs={"parent": self._uuid, "mode": self.PRINTER_MODE_DIALOG})

    @SIEffect.on_enter(E.capability.print_printer_selected, SIEffect.RECEPTION)
    def on_printer_selected_enter_recv(self, printer_name: str) -> None:
        self.selected_printer = printer_name

    @SIEffect.on_leave(E.capability.print_printer_selected, SIEffect.RECEPTION)
    def on_printer_selected_leave_recv(self) -> None:
        self.selected_printer = None

    @SIEffect.on_enter(E.capability.print_printer_mode_selected, SIEffect.RECEPTION)
    def on_printer_mode_selected_enter_emit(self, mode: str) -> None:
        self.selected_print_mode = mode

    @SIEffect.on_leave(E.capability.print_printer_mode_selected, SIEffect.RECEPTION)
    def on_printer_mode_selected_leave_recv(self) -> None:
        self.selected_print_mode = None

    @SIEffect.on_enter(E.capability.print_print_request, SIEffect.RECEPTION)
    def on_print_request_enter_recv(self, file_path: str) -> None:
        if self.selected_printer is None:
            return

        if self.selected_print_mode is None:
            self.run_in_thread(self.print_without_dialog, (file_path,))

        if self.selected_print_mode == E.id.print_dialog:
            self.run_in_thread(self.print_with_standard_app_dialog, (file_path,))

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self) -> tuple:
        rel_x = self.x - self.last_x
        rel_y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return rel_x, rel_y, self.x, self.y

    def print_without_dialog(self, filepath: str) -> None:
        # os.system(E.id.print_linux_command_lp_d + printer_name + ' ' + file_path) # direct way of printing -> via printer name
        print("Execute: ", E.id.print_linux_command_lp_d + " "+ self.selected_printer + ' ' + filepath)

    def print_with_standard_app_dialog(self, filepath: str) -> None:
        # Popen([E.id.print_linux_command_xdg_open + " " + file_path], stdin=PIPE, shell=True, start_new_session=True)
        # time.sleep(1)
        # pyautogui.hotkey(E.id.print_linux_command_hotkey_ctrl, E.id.print_linux_command_hotkey_p)
        print("Execute: ", E.id.print_linux_command_xdg_open + ' ' + filepath)
        print("sleep(1)")
        time.sleep(1)
        print(f"Press {E.id.print_linux_command_hotkey_ctrl}+{E.id.print_linux_command_hotkey_p}")
