import threading

from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
import time
import playsound
import os


class JingleObserver(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ JingleObserver __"
    region_display_name = "JingleObserver"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(JingleObserver, self).__init__(shape, uuid, "res/notes.png", JingleObserver.regiontype, JingleObserver.regionname, kwargs)
        self.qml_path = self.set_QML_path("JingleObserver.qml")
        self.sequence = ["A", "B", "C", "D", "E", "F", "G"]
        self.played_notes = []
        self.start_note_to_play = "A"
        self.note_to_play = self.start_note_to_play
        self.set_QML_data("reset", False, PySI.DataType.BOOL)
        self.thread_running = False

    def register_played_sound(self, note):
        self.set_QML_data("reset", False, PySI.DataType.BOOL)

        if note == self.note_to_play:
            self.note_to_play = self.sequence[self.sequence.index(note) + 1] if self.sequence.index(note) + 1 < len(self.sequence) else ""
            self.played_notes.append(note)

            self.set_QML_data(f"hit_j{len(self.played_notes)}", True, PySI.DataType.BOOL)
            self.set_QML_data(f"correct_j{len(self.played_notes)}", True, PySI.DataType.BOOL)

            if len(self.played_notes) == len(self.sequence):
                win = True

                for pn, sn in zip(self.played_notes, self.sequence):
                    if pn != sn:
                        win = False
                        break

                if win:
                    threading.Thread(target=self.play_jingle).start()

        else:
            self.played_notes.append(note)
            self.set_QML_data(f"hit_j{len(self.played_notes)}", True, PySI.DataType.BOOL)
            self.set_QML_data(f"correct_j{len(self.played_notes)}", False, PySI.DataType.BOOL)

            threading.Thread(target=self.reset).start()


    def reset(self):
        if not self.thread_running:
            self.thread_running = True
            time.sleep(2.0)

            for i in range(1, 8):
                self.set_QML_data(f"hit_j{i}", False, PySI.DataType.BOOL)
                self.set_QML_data(f"correct_j{i}", False, PySI.DataType.BOOL)

            self.note_to_play = self.sequence[0]
            self.played_notes = []
            self.note_to_play = self.start_note_to_play

            self.set_QML_data("reset", True, PySI.DataType.BOOL)
            self.thread_running = False

    def play_jingle(self):
        time.sleep(1.5)

        for note in self.sequence:
            time.sleep(0.3)
            file = os.getcwd() + f"/plugins/study/pde/res/xylophone-{note.lower()}.wav"
            playsound.playsound(file, block=False)