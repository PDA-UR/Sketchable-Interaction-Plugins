from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task9(Task):
    """
    DELETE the SUBFOLDER VL in FOLDER Tutorium/EIMI
    """
    def __init__(self, participant, repetition):
        super().__init__("9", participant, repetition)
        self.target_folder = self.root_path + "/Studium/Tutorium/Einführung MI/"

    #provide task message here
    def task_message(self):
        return "DELETE the SUBFOLDER \"Vorlesung\" in FOLDER \"Tutorium/Einführung MI\""

    # provide task implementation here
    def task_solution(self):
        return len([p.name for p in Path(self.target_folder).rglob("Vorlesung")]) == 0