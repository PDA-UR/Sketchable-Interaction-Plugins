from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E


class EmailContact(Movable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ EmailContact __"
    region_display_name = "EmailContact"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(EmailContact, self).__init__(shape, uuid, "", EmailContact.regiontype, EmailContact.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 255)
        self.qml_path = self.set_QML_path("EmailContact.qml")
        self.with_border = True
        self.border_width = 2
        self.parent = kwargs["parent"]
        self.contact_name = kwargs["contact"]
        self.parent.contacts.append(self)
        self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.set_QML_data("contact", self.contact_name, PySI.DataType.STRING)
        pass

    @SIEffect.on_enter("__CONTACT_ADD__", SIEffect.EMISSION)
    def on_contact_add_enter_emit(self, other):
        return self.contact_name

    @SIEffect.on_leave("__CONTACT_ADD__", SIEffect.EMISSION)
    def on_contact_add_leave_emit(self, other):
        return self.contact_name
