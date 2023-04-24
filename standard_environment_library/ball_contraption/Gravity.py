from libPySI import PySI

from plugins.standard_environment_library.ball_contraption.physics_mixins.GravitationalForceApplier import GravitationalForceApplier


class Gravity(GravitationalForceApplier):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Gravity __"
    region_display_name = "Gravity"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        kwargs["gravity"] = (0, -1000)
        super(Gravity, self).__init__(shape, uuid, "", Gravity.regiontype, Gravity.regionname, kwargs)
        pass