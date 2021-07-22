from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.button import Button


class Presentation(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ Presentation __"
    region_display_name = "Presentation"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(Presentation, self).__init__(shape, uuid, "res/presentation.png", Presentation.regiontype, Presentation.regionname, kwargs)
        self.source = "libStdSI"
        self.qml_path = self.set_QML_path("Presentation.qml")
        self.slides = []
        self.btns = []
        self.current_slide = 0
        self.is_open_entry_capability_blocked = True
        self.color = PySI.Color(156, 0, 75, 255)

    @SIEffect.on_enter("__PRESENT__", SIEffect.RECEPTION)
    def on_present_enter_recv(self, slides: list) -> None:
        if len(self.slides) == 0:
            self.slides = [slide for slide in slides if ".png" in slide or ".jpg" in slide or ".jpeg" in slide]
            if len(self.slides) > 0:
                self.color = PySI.Color(156, 0, 75, 128)

                x = self.relative_x_pos()
                y = self.relative_y_pos()

                self.shape = PySI.PointVector([[x, y], [x, y + 720], [x + 1280, y + 720], [x + 1280, y]])

                self.width = self.get_region_width()
                self.height = self.get_region_height()

                self.set_QML_data("img_path", self.slides[self.current_slide], PySI.DataType.STRING)
                self.set_QML_data("container_width", self.width, PySI.DataType.INT)
                self.set_QML_data("img_width", self.width, PySI.DataType.INT)
                self.set_QML_data("container_height", self.height, PySI.DataType.INT)
                self.set_QML_data("img_height", self.height, PySI.DataType.INT)
                self.set_QML_data("is_slide", True, PySI.DataType.BOOL)
                self.set_QML_data("page", f"{self.current_slide + 1}/{len(self.slides)}", PySI.DataType.STRING)

                if len(slides) > 1:
                    self.add_buttons()


    @SIEffect.on_enter(PySI.CollisionCapability.PARENT, SIEffect.EMISSION)
    def on_parent_enter_emit(self, other: object) -> str:
        self.btns.append(other)
        return self._uuid

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_continuous(PySI.CollisionCapability.BTN, SIEffect.RECEPTION)
    def on_btn_continuous_recv(self, cursor_id: str, value: bool) -> None:
        if cursor_id != "" and value != "":
            self.on_btn_trigger(cursor_id, value)

    def add_buttons(self) -> None:
        x = self.absolute_x_pos()
        y = self.absolute_y_pos()

        horizontal_margin = 10
        vertical_margin = 10

        btn_width = Button.Button.region_width
        btn_height = Button.Button.region_height

        shape_btn1 = [[x + self.width - btn_width - horizontal_margin, y + self.height - btn_height - vertical_margin],
                      [x + self.width - btn_width - horizontal_margin, y + self.height - vertical_margin],
                      [x + self.width - horizontal_margin, y + self.height - vertical_margin],
                      [x + self.width - horizontal_margin, y + self.height - btn_height - vertical_margin]]

        kwargs_btn1 = {}
        kwargs_btn1["parent"] = self._uuid
        kwargs_btn1["value"] = False

        self.create_region_via_id(shape_btn1, PySI.EffectType.SI_BUTTON, kwargs_btn1)

        shape_btn2 = [[x + horizontal_margin, y + self.height - btn_height - vertical_margin],
                      [x + horizontal_margin, y + self.height - vertical_margin],
                      [x + btn_width + horizontal_margin, y + self.height - vertical_margin],
                      [x + btn_width + horizontal_margin, y + self.height - btn_height - vertical_margin]]

        kwargs_btn2 = {}
        kwargs_btn2["parent"] = self._uuid
        kwargs_btn2["value"] = True

        self.create_region_via_id(shape_btn2, PySI.EffectType.SI_BUTTON, kwargs_btn2)

    def on_btn_trigger(self, sender: str, value: bool) -> None:
        last_slide = self.current_slide

        if value:
            self.current_slide = self.current_slide - 1 if self.current_slide > 0 else self.current_slide if value else self.current_slide + 1 if self.current_slide + 1 < len(self.slides) else self.current_slide
        else:
            self.current_slide = self.current_slide + 1 if self.current_slide + 1 < len(self.slides) else self.current_slide

        if last_slide != self.current_slide:
            self.set_QML_data("img_path", self.slides[self.current_slide], PySI.DataType.STRING)
            self.set_QML_data("page", f"{self.current_slide + 1}/{len(self.slides)}", PySI.DataType.STRING)

    def delete(self) -> None:
        for btn in self.btns:
            btn.delete()

        super().delete()
