from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task11(Task):
    """
    FIND an IMAGE FILE with a blue Bird as its content by NAVIGATING to FOLDER 2. Semester/Propädeutikum/Lesetexte and MOVE the IMAGE FILE with a blue Bird as its content to the FOLDER Studium"
    """
    def __init__(self, participant, repetition):
        super().__init__("11", participant, repetition)
        self.source_folder = self.root_path + "/Studium/2. Semester/Propädeutikum/Lesetexte"
        self.target_folder = self.root_path + "/Studium"

    #provide task message here
    def task_message(self):
        return "FIND an IMAGE FILE with a blue Bird as its content by NAVIGATING to FOLDER \"2. Semester/Propädeutikum/Lesetexte\"and MOVE the IMAGE FILE with a blue Bird as its content to the FOLDER \"Studium\""

    # provide task implementation here
    def task_solution(self):
        return len([p.name for p in Path(self.source_folder).rglob("blauer_vogel.jpg")]) == 0 and len([p.name for p in Path(self.target_folder).rglob("blauer_vogel.jpg")]) == 1