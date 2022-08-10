from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task3(Task):
    """
    DELETE all FILES which are zip FILES from FOLDER OOP
    """
    def __init__(self, participant, repetition):
        super().__init__("3", participant, repetition)
        self.source_folder = "Studium/1. Semester/OOP"
        self.source_files = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if ".zip" in t]

    #provide task message here
    def task_message(self):
        return "DELETE all FILES which are zip FILES from FOLDER OOP"

    # provide task implementation here
    def task_solution(self):
        # OOP Folder still there
        if not os.path.isdir(self.root_path + "/" + self.source_folder):
            return False

        # ZIP files gone from File System
        zips = [p.name for p in Path(self.root_path + "/Studium").rglob("*.zip")]

        for f in self.source_files:
            if f in zips:
                return False

        return True