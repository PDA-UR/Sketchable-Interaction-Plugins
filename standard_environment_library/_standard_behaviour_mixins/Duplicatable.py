from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
import inspect


class Duplicatable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__DELETABLE__"

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super().__init__(shape, uuid, r, t, s, kwargs)

        self.is_duplicate = False
        self.duplicate_offset = 10, 10

        if type(self).handle_duplication == Duplicatable.handle_duplication:
            raise NotImplementedError(f"Overwrite method handle_duplication in {type(self)}!")

        if type(self).on_duplicate_enter_recv == Duplicatable.on_duplicate_enter_recv:
            raise NotImplementedError(f"Overwrite method on_duplicate_enter_recv in {type(self)}!")

        pass

    def handle_duplication(self, kwargs):
        pass

    def target_data(self):
        return {k: getattr(self, k) for k in dir(self)}

    def qml_data(self, clazz):
        return self.__default_qml_calls__() + self.__qml_calls__(inspect.getsource(clazz))

    @SIEffect.on_enter("__ DUPLICATE __", SIEffect.RECEPTION)
    def on_duplicate_enter_recv(self):
        pass

    @SIEffect.on_leave("__ DUPLICATE __", SIEffect.RECEPTION)
    def on_duplicate_leave_recv(self):
        self.is_duplicate = False

    def __qml_calls__(self, source):
        ret = []
        calls = self.__find_all_qml_occurrences__(source, "self.set_QML_data")

        for call in calls:
            s = source[call:source.find("\n", call)]
            key = s[s.find("(") + 1:s.find(",")][1:-1]
            dtype_str = s[s.rfind(",") + 1:s.rfind(")")].strip()

            if dtype_str[0] != "P":
                continue

            dtype = eval(dtype_str)
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