from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

class Preview(Deletable, Movable, SIEffect):
    regiontype = PySI.EffectType.SI_PREVIEW
    regionname = PySI.EffectName.SI_STD_NAME_PREVIEW
    region_display_name = E.id.preview_display_name

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super(Preview, self).__init__(shape, uuid, E.id.preview_texture, Preview.regiontype, Preview.regionname, kwargs)
        self.qml_path = self.set_QML_path(E.id.preview_qml_file_name)
        self.color = E.id.preview_color

    @SIEffect.on_enter(E.id.preview_capability_previewing, SIEffect.EMISSION)
    def on_preview_enter_emit(self, other):
        pass

    @SIEffect.on_leave(E.id.preview_capability_previewing, SIEffect.EMISSION)
    def on_preview_leave_emit(self, other):
        pass