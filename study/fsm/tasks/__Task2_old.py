from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path

class Task2(Task):
    """
    CREATE a new FOLDER structure for the FOLDER "Mathematik II" in FOLDER "2. Semester". It should follow the structure of FOLDER "Mathematik I", including SUBFOLDERS.
    """
    def __init__(self, participant, repetition):
        super().__init__("2", participant, repetition)
        self.source_folder = "Studium/1. Semester/Mathematik I"
        self.target_folder = "Studium/2. Semester/Mathematik II"
        self.target_subfolder = "Zusatzmaterial"

    #provide task message here
    def task_message(self):
        return "CREATE a new FOLDER structure for the FOLDER \"Mathematik II\" in FOLDER \"2. Semester\". It should follow the structure of FOLDER \"Mathematik I\", including SUBFOLDERS."

    # provide task implementation here
    def task_solution(self):
        is_vl_u_zm_present = len([p.name for p in Path(self.root_path + "/" + self.target_folder).glob("*") if p.name == "Vorlesung" or p.name == "Zusatzmaterial" or p.name == "Übung"])
        is_c_lt_in_zm_present = len([p.name for p in Path(self.root_path + "/" + self.target_folder + "/" + self.target_subfolder).glob("*") if p.name == "Code" or p.name == "Lesetexte"])

        return is_vl_u_zm_present == 3 and is_c_lt_in_zm_present == 2