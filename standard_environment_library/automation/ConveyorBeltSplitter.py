from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class ConveyorBeltSplitter(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.cb_splitter_name
    region_display_name = E.id.cb_splitter_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(ConveyorBeltSplitter, self).__init__(shape, uuid, E.id.cb_splitter_texture, ConveyorBeltSplitter.regiontype, ConveyorBeltSplitter.regionname, kwargs)

        self.qml_path = self.set_QML_path(E.id.cb_splitter_qml_file_path)
        self.color = E.color.cb_splitter_color
        self.io_width = E.id.cb_width * E.id.cb_splitter_io_width_multiplier
        self.output_point_true = None
        self.output_point_false = None

        self.reshape()

        self.set_QML_data("conditions", self.conditional_variables(), PySI.DataType.LIST)

    def reshape(self):
        self.shape = PySI.PointVector([
            [self.relative_x_pos(), self.relative_y_pos()],
            [self.relative_x_pos() + self.io_width, self.relative_y_pos()],
            [self.relative_x_pos() + self.io_width, self.relative_y_pos() - self.io_width],
            [self.relative_x_pos() + self.io_width * 2, self.relative_y_pos() - self.io_width],
            [self.relative_x_pos() + self.io_width * 2, self.relative_y_pos() + self.io_width * 2],
            [self.relative_x_pos() + self.io_width, self.relative_y_pos() + self.io_width * 2],
            [self.relative_x_pos() + self.io_width, self.relative_y_pos() + self.io_width],
            [self.relative_x_pos(), self.relative_y_pos() + self.io_width],
        ])

        self.width = self.get_region_width()
        self.height = self.get_region_height()

        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

        self.output_point_true = (self.relative_x_pos() + self.io_width) + (((self.relative_x_pos() + self.io_width * 2) - (self.relative_x_pos() + self.io_width)) / 2), self.relative_y_pos() - self.io_width
        self.output_point_false = (self.relative_x_pos() + self.io_width) + (((self.relative_x_pos() + self.io_width * 2) - (self.relative_x_pos() + self.io_width)) / 2), self.relative_y_pos() + self.io_width * 2

    @SIEffect.on_enter(E.capability.cb_splitter_evaluate, SIEffect.EMISSION)
    def on_cb_splitter_evaluate_enter_emit(self, other):
        try:
            eval("other." + self.get_QML_data(E.id.cb_splitter_text_from_qml, PySI.DataType.STRING))
            return self._uuid, self.output_point_true[0] - other.width / 2 - other.relative_x_pos(), self.output_point_true[1] + other.height / 4 - other.relative_y_pos()
        except:
            return self._uuid, self.output_point_false[0] - other.width / 2 - other.relative_x_pos(), self.output_point_false[1] + other.height / 2 - other.relative_y_pos()

    # overrides Movable class implementation
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        Movable.set_position_from_position(self, rel_x, rel_y, abs_x, abs_y)

        self.output_point_true = self.output_point_true[0] + rel_x, self.output_point_true[1] + rel_y
        self.output_point_false = self.output_point_false[0] + rel_x, self.output_point_false[1] + rel_y
