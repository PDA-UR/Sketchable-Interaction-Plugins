from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E

import math

class ConveyorBeltMerger(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = E.id.cb_merger_name
    region_display_name = E.id.cb_merger_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        Deletable.__init__(self, shape, uuid, E.id.cb_merger_texture, ConveyorBeltMerger.regiontype, ConveyorBeltMerger.regionname, kwargs)
        Movable.__init__(self, shape, uuid, E.id.cb_merger_texture, ConveyorBeltMerger.regiontype, ConveyorBeltMerger.regionname, kwargs)
        SIEffect.__init__(self, shape, uuid, E.id.cb_merger_texture, ConveyorBeltMerger.regiontype, ConveyorBeltMerger.regionname, kwargs)

        self.qml_path = self.set_QML_path(E.id.cb_merger_qml_file_path)
        self.color = E.id.cb_merger_color
        self.output_width = E.id.cb_width * E.id.cb_splitter_io_width_multiplier
        self.output_point = None

        self.reshape()

    def reshape(self):
        height = width = 200
        offset = (width - self.output_width) / 2

        self.shape = PySI.PointVector([
            [self.relative_x_pos(), self.relative_y_pos()],
            [self.relative_x_pos() + width, self.relative_y_pos()],
            [self.relative_x_pos() + width, self.relative_y_pos() + height],
            [self.relative_x_pos() + width - offset, self.relative_y_pos() + height],
            [self.relative_x_pos() + width - offset, self.relative_y_pos() + height + self.output_width],
            [self.relative_x_pos() + offset, self.relative_y_pos() + height + self.output_width],
            [self.relative_x_pos() + offset, self.relative_y_pos() + height],
            [self.relative_x_pos(), self.relative_y_pos() + height],
       ])

        self.width = self.get_region_width()
        self.height = self.get_region_height()

        self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
        self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

        self.output_point = self.relative_x_pos() + offset + self.output_width / 2, self.relative_y_pos() + height + self.output_width

    @SIEffect.on_enter(E.id.cb_merger_evaluate_capability, SIEffect.EMISSION)
    def on_cb_merger_evaluate_enter_emit(self, other):
        return self._uuid, self.output_point[0] - other.width / 2 - other.relative_x_pos(), self.output_point[1] - other.height / 4 - other.relative_y_pos()

    # overrides Movable class implementation
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        Movable.set_position_from_position(self, rel_x, rel_y, abs_x, abs_y)

        self.output_point = self.output_point[0] + rel_x, self.output_point[1] + rel_y
