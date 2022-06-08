from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.study.fsm.tasks.__Task1 import Task1


class FSMLogging(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FSMLogging __"
    region_display_name = "FSMLogging"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FSMLogging, self).__init__(shape, uuid, "", FSMLogging.regiontype, FSMLogging.regionname, kwargs)
        self.color = PySI.Color(0, 0, 0, 0)
        self.task = eval(f"Task{kwargs['task']}(kwargs[\"participant\"], kwargs[\"repetition\"])")
