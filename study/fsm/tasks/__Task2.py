from plugins.study.fsm.tasks.__Task import Task
import os


class Task2(Task):
    """
    MOVE the content of FOLDER ”Einführung MI” into three newly CREATED FOLDERS ”Vorlesung”, ”Übung”, ”Lesetexte”
    """
    def __init__(self, participant, repetition):
        super().__init__("2", participant, repetition)

        self.source_folder = "Studium/1. Semester/Einführung MI"

    #provide task message here
    def task_message(self):
        return "MOVE the content of FOLDER \"Studium/1. Semester/Einführung MI\" into three newly CREATED FOLDERS for \"Vorlesung\", \"Übung\", and \"Lesetexte\", according to naming of the contents."

    # provide task implementation here
    def task_solution(self):
        fs = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if ("Übung" in t or "Vorlesung" in t or "Lesetexte" in t) and not ".pdf" in t]
        su = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if "Übung" in t and ".pdf" in t]
        sv = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if "Vorlesung" in t and ".pdf" in t]
        st = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if "Lesetext" in t and ".pdf" in t]

        if "Vorlesung" not in fs or "Übung" not in fs or "Lesetexte" not in fs:
            return False

        target_vl = [t for t in os.listdir(self.root_path + "/" + self.source_folder + "/Vorlesung") if "Vorlesung" in t and ".pdf" in t]
        target_ue = [t for t in os.listdir(self.root_path + "/" + self.source_folder + "/Übung") if "Übung" in t and ".pdf" in t]
        target_lt = [t for t in os.listdir(self.root_path + "/" + self.source_folder + "/Lesetexte") if "Lesetext" in t and ".pdf" in t]

        for tsu in su:
            if tsu not in target_ue:
                return False

        for tsv in sv:
            if tsv not in target_vl:
                return False

        for tst in st:
            if tst not in target_lt:
                return False

        for t in su + sv + st:
            if t in os.listdir(self.root_path + "/" + self.source_folder):
                return False

        return True