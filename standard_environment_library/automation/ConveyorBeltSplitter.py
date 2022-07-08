from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.automation.CBSplitterConditionalVariable import CBSplitterConditionalVariable
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
        self.current_conditional_variable = "none"
        cond_vars = self.conditional_variables()
        cond_vars.remove("<condition>")
        self.no_entry_image = "res/no_entry.png"
        cw, ch = self.context_dimensions()
        self.start_y_cond_vars = 0 * ch / 1080
        self.cond_var_width = cw / 16
        self.yoffset = ch / 216
        self.xoffset = cw / 48
        self.cond_var_height = (self.height - self.start_y_cond_vars - self.yoffset * len(cond_vars)) / len(cond_vars)
        self.cond_vars = []
        if not "is_selector" in kwargs or not kwargs["is_selector"]:
            for i, cv in enumerate(cond_vars):
                x, y = self.aabb[0].x + self.x + self.width + self.xoffset / 2, self.aabb[0].y + self.y + self.start_y_cond_vars + i * (self.cond_var_height + self.yoffset)
                shape = [[x, y], [x, y + self.cond_var_height], [x + self.cond_var_width - self.xoffset, y + self.cond_var_height], [x + self.cond_var_width - self.xoffset, y]]
                self.create_region_via_name(PySI.PointVector(shape), CBSplitterConditionalVariable.regionname, False, {"parent": self, "identifier": cv})

        self.set_QML_data("no_entry_image", self.no_entry_image, PySI.DataType.STRING)

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

    @SIEffect.on_enter("__CONDITIONAL_VARIABLE_ADD__", SIEffect.RECEPTION)
    def on_conditional_variable_add_enter_recv(self, current_conditional_variable, icon):
        self.current_conditional_variable = current_conditional_variable
        self.set_QML_data("entry_image", icon, PySI.DataType.STRING)
        self.set_QML_data("entry_image_visible", True, PySI.DataType.BOOL)

    @SIEffect.on_leave("__CONDITIONAL_VARIABLE_ADD__", SIEffect.RECEPTION)
    def on_conditional_variable_add_leave_recv(self, current_conditional_variable, icon):
        if self.current_conditional_variable == current_conditional_variable:
            self.current_conditional_variable = "None"
            self.set_QML_data("entry_image_visible", False, PySI.DataType.BOOL)

    @SIEffect.on_enter(E.capability.cb_splitter_evaluate, SIEffect.EMISSION)
    def on_cb_splitter_evaluate_enter_emit(self, other):
        try:
            eval("other." + self.current_conditional_variable)
            return self._uuid, self.output_point_true[0] - other.width / 2 - other.relative_x_pos(), self.output_point_true[1] + other.height / 4 - other.relative_y_pos()
        except:
            return self._uuid, self.output_point_false[0] - other.width / 2 - other.relative_x_pos(), self.output_point_false[1] + other.height / 2 - other.relative_y_pos()

    # overrides Movable class implementation
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        Movable.set_position_from_position(self, rel_x, rel_y, abs_x, abs_y)

        self.output_point_true = self.output_point_true[0] + rel_x, self.output_point_true[1] + rel_y
        self.output_point_false = self.output_point_false[0] + rel_x, self.output_point_false[1] + rel_y

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        for item in self.cond_vars:
            item.delete()
        self.delete()