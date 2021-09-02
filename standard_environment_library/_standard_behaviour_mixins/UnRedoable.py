from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect

from copy import deepcopy
import inspect

from plugins.E import E

class UnRedoable(SIEffect):
    """
    Local Linear Multi-Level Memento
    """
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ UnRedoable __"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super().__init__(shape, uuid, r, t, s, kwargs)

        self.__stack__ = []
        self.__current__ = {}
        self.__stack_idx__ = 0

    @staticmethod
    def action(f):
        def wrap(*args, **kwargs):
            f(*args, **kwargs)
            self = args[0]
            qml = self.__default_qml_calls__() + self.__qml_calls__(inspect.getsource(f))
            self.__register__(qml)
        return wrap

    def __qml_calls__(self, source):
        ret = []
        calls = self.__find_all_qml_occurrences__(source, "self.set_QML_data")

        for call in calls:
            s = source[call:source.find("\n", call)]
            key = s[s.find("(") + 1:s.find(",")][1:-1]
            dtype = eval(s[s.rfind(",") + 1:s.find(")")].strip())
            value = self.get_QML_data(key, dtype)

            ret.append([key, value, dtype])

        return ret

    def __default_qml_calls__(self):
        ret = []
        if self.texture_path != "":
            # SIEffect standard
            standard_qml = [{"img_width": PySI.DataType.INT},
                            {"img_height": PySI.DataType.INT},
                            {"img_path": PySI.DataType.STRING},
                            {"widget_width": PySI.DataType.FLOAT},
                            {"widget_height": PySI.DataType.FLOAT},
                            {"uuid": PySI.DataType.STRING}
                            ]

            for d in standard_qml:
                for key, dtype in d.items():
                    value = self.get_QML_data(key, dtype)

                    ret.append([key, value, dtype])

        return ret

    def __find_all_qml_occurrences__(self, s, sub):
        return [i for i in range(len(s)) if s.startswith(sub, i)]

    def __add_to_stack__(self, qml: list):
        target_data = {k: getattr(self, k) for k in dir(self)}

        del target_data["__stack__"]
        del target_data["__stack_idx__"]
        del target_data["__current__"]
        del target_data["__add_to_stack__"]
        del target_data["__save__"]
        del target_data["__register__"]
        del target_data["cap_emit"]
        del target_data["cap_recv"]
        del target_data["cap_link_emit"]
        del target_data["cap_link_recv"]
        del target_data["__dict__"]

        self.__current__ = {"qml": qml}
        for k, v in target_data.items():
            if not callable(v):
                self.__current__[k] = v

        self.__save__()

    def __save__(self):
        if self.__stack_idx__ < len(self.__stack__) - 1:
            self.__stack__ = self.__stack__[0:self.__stack_idx__ + 1]

        self.__stack_idx__ = len(self.__stack__)
        self.__stack__.append(deepcopy(self.__current__))

    def __undo__(self):
        if len(self.__stack__) > 0:
            self.__stack_idx__ = self.__stack_idx__ - 1 if self.__stack_idx__ > 0 else 0
            self.__current__ = self.__stack__[self.__stack_idx__]

        for k, v in self.__current__.items():
            if k != "qml":
                setattr(self, k, v)
            else:
                for e in v:
                    self.set_QML_data(*e)

    def __redo__(self):
        print(self.__stack_idx__)

        self.__stack_idx__ = self.__stack_idx__ + 1 if self.__stack_idx__ < len(self.__stack__) - 1 else len(self.__stack__) - 1
        self.__stack_idx__ = 0 if self.__stack_idx__ < 0 else self.__stack_idx__

        print(self.__stack_idx__)

        self.__current__ = self.__stack__[self.__stack_idx__]

        for k, v in self.__current__.items():
            if k != "qml":
                setattr(self, k, v)
            else:
                for e in v:
                    self.set_QML_data(*e)

    def __register__(self, qml: list):
        self.__add_to_stack__(qml)

    @SIEffect.on_enter(E.capability.undo_undo, SIEffect.RECEPTION)
    def __on_undo_enter_recv__(self):
        self.__undo__()

    @SIEffect.on_enter(E.capability.redo_redo, SIEffect.RECEPTION)
    def __on_redo_enter_recv__(self):
        self.__redo__()

