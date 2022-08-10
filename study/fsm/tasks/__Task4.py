from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task4(Task):
    """
    DELETE all FILES and FOLDERS which have ”temp” in their names from FOLDER Studium and its SUBFOLDERS
    """
    def __init__(self, participant, repetition):
        super().__init__("4", participant, repetition)

    #provide task message here
    def task_message(self):
        return "DELETE all FILES and FOLDERS which have \"temp\" in their names from FOLDER \"Studium\" and its SUBFOLDERS"

    # provide task implementation here
    def task_solution(self):
        return len([p.name for p in Path(self.root_path + "/Studium").rglob("*temp*")]) == 0