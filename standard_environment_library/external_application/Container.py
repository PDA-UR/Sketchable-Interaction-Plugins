from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
import math


class Container(SIEffect):
    regiontype = PySI.EffectType.SI_EXTERNAL_APPLICATION_CONTAINER
    regionname = PySI.EffectName.SI_STD_NAME_CONTAINER

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Container, self).__init__(shape, uuid, self.TEXTURE_PATH_NONE, Container.regiontype, Container.regionname, kwargs)
        self.color = PySI.Color(128, 128, 128, 128)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.GEOMETRY, PySI.LinkingCapability.GEOMETRY)
    def set_geometry_from_geometry(self, abs_x, abs_y, width, height):
        if self.width == width and self.height == height:
            self.move(abs_x, abs_y)
        else:
            self.has_data_changed = True
            self.move(0, 0)
            # self.move(abs_x - abs(abs_x - self.x), abs_y)

            self.shape = PySI.PointVector([[abs_x - 5, abs_y - 5], [abs_x - 5, abs_y + height + 30], [abs_x + width + 5, abs_y + height + 30], [abs_x + width + 5, abs_y - 5]])
