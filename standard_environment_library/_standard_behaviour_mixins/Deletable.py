from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class Deletable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__DELETABLE__"

    @staticmethod
    def unredoable(f):
        def wrap(*args, **kwargs):
            f(*args)
            args[0].__unredoable_deletion__ = True
        return wrap

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Deletable, self).__init__(shape, uuid, r, t, s, kwargs)

    @SIEffect.on_enter(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_enter_recv(self):
        if not self.is_under_user_control:
            self.delete()

    @SIEffect.on_continuous(PySI.CollisionCapability.DELETION, SIEffect.RECEPTION)
    def on_deletion_continuous_recv(self):
        if not self.is_under_user_control:
            self.delete()