from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable


class Palette(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_PALETTE
    regionname = PySI.EffectName.SI_STD_NAME_PALETTE

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Palette, self).__init__(shape, uuid, "", Palette.regiontype, Palette.regionname, kwargs)

        available_plugins = self.available_plugins()
        excluded_plugins = self.excluded_plugins()

        for ep in excluded_plugins:
            available_plugins.remove(ep)

        self.color = E.id.palette_color

        self.as_selector = True
        self.num_selectors_per_row = int(len(available_plugins) / 3) + 1

        if len(available_plugins) % self.num_selectors_per_row == 0:
            self.num_rows = len(available_plugins) / self.num_selectors_per_row
        else:
            self.num_rows = int(len(available_plugins) / self.num_selectors_per_row) + 1

        self.x_offset = E.id.palette_selector_x_offset
        self.y_offset = E.id.palette_selector_y_offset

        self.selector_width = E.id.palette_selector_width
        self.selector_height = E.id.palette_selector_height

        y = -1
        x = 1

        for i in range(len(available_plugins)):
            if i % self.num_selectors_per_row:
                x += 1
            else:
                x = x - self.num_selectors_per_row - 1 if x - self.num_selectors_per_row - 1 >= 0 else 0
                y += 1

            shape = [[((self.x_offset + self.selector_width) * x) + (self.relative_x_pos() + self.x_offset), ((self.y_offset + self.selector_height) * y) + (self.relative_y_pos() + self.y_offset)],
                     [((self.x_offset + self.selector_width) * x) + (self.relative_x_pos() + self.x_offset), ((self.y_offset + self.selector_height) * y) + (self.relative_y_pos() + self.y_offset + self.selector_height)],
                     [((self.x_offset + self.selector_width) * x) + (self.relative_x_pos() + self.x_offset + self.selector_width), ((self.y_offset + self.selector_height) * y) + (self.relative_y_pos() + self.y_offset + self.selector_height)],
                     [((self.x_offset + self.selector_width) * x) + (self.relative_x_pos() + self.x_offset + self.selector_width), ((self.y_offset + self.selector_height) * y) + (self.relative_y_pos() + self.y_offset)]]

            self.create_region_via_name(shape, available_plugins[i], self.as_selector, {"parent": self._uuid})

        self.shape = PySI.PointVector([[self.relative_x_pos(), self.relative_y_pos()],
                                       [self.relative_x_pos(), self.relative_y_pos() + ((y + 1) * self.selector_height + 4 * self.y_offset)],
                                       [self.relative_x_pos() + (self.num_selectors_per_row * self.selector_width + 4 * self.x_offset), self.relative_y_pos() + ((y + 1) * self.selector_height + 4 * self.y_offset)],
                                       [self.relative_x_pos() + (self.num_selectors_per_row * self.selector_width + 4 * self.x_offset), self.relative_y_pos()]])


    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y

        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y