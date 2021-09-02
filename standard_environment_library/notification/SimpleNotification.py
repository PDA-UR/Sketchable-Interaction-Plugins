from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class SimpleNotification(SIEffect):
    regiontype = PySI.EffectType.SI_NOTIFICATION
    regionname = PySI.EffectName.SI_STD_NAME_SIMPLE_NOTIFICATION
    region_width = E.id.notification_region_width
    region_height = E.id.notification_region_height

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(SimpleNotification, self).__init__(shape, uuid, "", SimpleNotification.regiontype, SimpleNotification.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.notification_qml_file_name)
        self.color = E.color.notification_color
        self.message = E.id.notification_default_message

        self.width = SimpleNotification.region_width
        self.height = SimpleNotification.region_height

        self.set_QML_data("containerwidth", self.width, PySI.DataType.INT)
        self.set_QML_data("containerheight", self.height, PySI.DataType.INT)
        self.set_QML_data("text", self.message, PySI.DataType.STRING)

    def update_message(self, message):
        self.message = message
        self.set_QML_data("message", self.message, PySI.DataType.STRING)
