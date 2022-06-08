from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.email.EmailContact import EmailContact
from plugins.E import E


class SendEmail(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM
    regionname = "__ SendEmail __"
    region_display_name = "Send Email"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(SendEmail, self).__init__(shape, uuid, "res/send_mail.png", SendEmail.regiontype, SendEmail.regionname, kwargs)
        self.color = PySI.Color(64, 224, 208, 255)
        self.qml_path = self.set_QML_path("SendEmail.qml")
        cw, ch = self.context_dimensions()

        contacts = ["Raphael Wimmer", "Andreas Schmid", "Vitus Maierhöfer", "Sarah Thanner"]

        self.start_y_contact_vars = 0 * ch / 1080
        self.contact_width = cw / 16
        self.yoffset = ch / 216
        self.xoffset = cw / 48
        self.contact_height = (self.height - self.start_y_contact_vars - self.yoffset * len(contacts)) / len(contacts)
        self.contacts = []
        self.current_contact = ""

        if not "is_selector" in kwargs or not kwargs["is_selector"]:
            for i, cv in enumerate(contacts):
                x, y = self.aabb[0].x + self.x + self.width + self.xoffset / 2, self.aabb[0].y + self.y + self.start_y_contact_vars + i * (self.contact_height + self.yoffset)
                shape = [[x, y], [x, y + self.contact_height], [x + self.contact_width - self.xoffset, y + self.contact_height], [x + self.contact_width - self.xoffset, y]]
                self.create_region_via_name(PySI.PointVector(shape), EmailContact.regionname, False, {"parent": self, "contact": cv})
        pass

    @SIEffect.on_enter("__CONTACT_ADD__", SIEffect.RECEPTION)
    def on_contact_add_enter_recv(self, contact):
        self.current_contact = contact
        self.set_QML_data("contact", self.current_contact, PySI.DataType.STRING)

    @SIEffect.on_leave("__CONTACT_ADD__", SIEffect.RECEPTION)
    def on_contact_add_leave_recv(self, contact):
        if contact == self.current_contact:
            self.current_contact = ""
            self.set_QML_data("contact", self.current_contact, PySI.DataType.STRING)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        x = self.x - self.last_x
        y = self.y - self.last_y
        self.last_x = self.x
        self.last_y = self.y

        return x, y, self.x, self.y

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        for item in self.contacts:
            item.delete()
        self.delete()