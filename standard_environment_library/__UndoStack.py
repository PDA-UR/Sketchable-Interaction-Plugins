from copy import deepcopy


class UndoStack:
    def __init__(self) -> None:
        self.__stack__ = [{"obj": None, "qml": None}, {"obj": None, "qml": None}]
        self.__current__ = {}
        self.__idx__ = 0

    def add(self, target: object) -> None:
        self.__current__ = {}

        if self.__idx__ < len(self.__stack__) - 1:
            self.__stack__ = self.__stack__[0:self.__idx__ + 1] + [{"obj": None, "qml": None}]

        self.__current__["obj"] = deepcopy(target)
        self.__current__["qml"] = {k: [target.get_QML_data(k, v), v] for k, v in target.__qml_data_keys_and_types__().items()}

        self.__stack__.insert(-1, deepcopy(self.__current__))
        self.__idx__ = len(self.__stack__)

    def get(self) -> tuple:
        return deepcopy(self.__current__["obj"]), deepcopy(self.__current__["qml"]), self.__current__["obj"] != None

    def undo(self) -> object:
        if len(self.__stack__) > 0:
            self.__idx__ = self.__idx__ - 1 if self.__idx__ > 0 else 0
            self.__current__ = self.__stack__[self.__idx__]

        return self

    def redo(self) -> object:
        self.__idx__ = self.__idx__ + 1 if self.__idx__ < len(self.__stack__) - 1 else len(self.__stack__) - 1
        self.__current__ = self.__stack__[self.__idx__]

        return self