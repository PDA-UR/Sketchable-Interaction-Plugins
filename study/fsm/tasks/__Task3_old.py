from plugins.study.fsm.tasks.__Task import Task
import os
import glob


class Task3(Task):
    """
    COPY all PDF-files with ”cheathsheet” in their names from FOLDER ”Mathematik I” to FOLDER ”Mathematik II”
    """
    def __init__(self, participant, repetition):
        super().__init__("3", participant, repetition)
        self.source_folder = "Studium/1. Semester/Mathematik I/"
        self.source_files = [t for t in [f for f in os.listdir(self.root_path + "/" + self.source_folder) if os.path.isfile(os.path.join(self.root_path + "/" + self.source_folder, f))] if "Cheatsheet" in t]
        self.target_folder = "Studium/2. Semester/Mathematik II/"

    #provide task message here
    def task_message(self):
        return "COPY all PDF-files with \"cheathsheet\" in their names from FOLDER \"Mathematik I\" to FOLDER \"Mathematik II\""

    # provide task implementation here
    def task_solution(self):
        target_files = [t for t in os.listdir(self.root_path + "/" + self.target_folder) if "Cheatsheet" in t]

        for s in self.source_files:
            if s not in target_files:
                return False

        return True