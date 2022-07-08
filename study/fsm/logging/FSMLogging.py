from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.study.fsm.tasks.__Task1 import Task1
from plugins.study.fsm.tasks.__Task2 import Task2
from plugins.study.fsm.tasks.__Task3 import Task3
from plugins.study.fsm.tasks.__Task4 import Task4
from plugins.study.fsm.tasks.__Task5 import Task5
from plugins.study.fsm.tasks.__Task6 import Task6
from plugins.study.fsm.tasks.__Task7 import Task7
from plugins.study.fsm.tasks.__Task8 import Task8
from plugins.study.fsm.tasks.__Task9 import Task9
from plugins.study.fsm.tasks.__Task10 import Task10
from plugins.study.fsm.tasks.__Task11 import Task11
from plugins.study.fsm.tasks.__Task12 import Task12


class FSMLogging(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ FSMLogging __"
    region_display_name = "FSMLogging"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(FSMLogging, self).__init__(shape, uuid, "", FSMLogging.regiontype, FSMLogging.regionname, kwargs)
        self.color = PySI.Color(0, 0, 0, 0)
        self.task = eval(f"Task{kwargs['task']}(kwargs[\"participant\"], kwargs[\"repetition\"])")
