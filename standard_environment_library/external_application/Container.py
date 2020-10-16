from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect


class Container(SIEffect):
    regiontype = PySI.EffectType.SI_EXTERNAL_APPLICATION_CONTAINER
    regionname = PySI.EffectName.SI_STD_NAME_CONTAINER

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Container, self).__init__(shape, uuid, self.TEXTURE_PATH_NONE, Container.regiontype, Container.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 0)

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.GEOMETRY, PySI.LinkingCapability.GEOMETRY)
    def set_geometry_from_geometry(self, abs_x, abs_y, width, height):
        if self.width == width and self.height == height:
            self.move(abs_x, abs_y)

            self.width = width
            self.height = height
        else:
            self.shape = PySI.PointVector([[abs_x, abs_y], [abs_x, abs_y + height], [abs_x + width, abs_y + height], [abs_x + width, abs_y]])
            self.has_data_changed = True
            self.x = abs_x
            self.y = abs_y
            self.width = width
            self.height = height
