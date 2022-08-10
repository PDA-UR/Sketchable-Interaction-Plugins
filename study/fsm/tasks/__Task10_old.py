from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task10(Task):
    """
    FIND an IMAGE FILE with the name usabilityproblemDerWoche3.jpg by NAVIGATING or SEARCHING and COPY the IMAGE FILE usabilityproblemDerWoche3.jpg to the FOLDER "Studium/Tutorium/Einführung MI"
    """
    def __init__(self, participant, repetition):
        super().__init__("10", participant, repetition)
        self.source_folder = self.root_path + "/Studium/Downloads"
        self.target_folder = self.root_path + "/Studium/Tutorium/Einführung MI/"
        self.target_file = "usabilityproblemDerWoche3.jpg"

    #provide task message here
    def task_message(self):
        return "FIND an IMAGE FILE with the name \"usabilityproblemDerWoche3.jpg\" by NAVIGATING to FOLDER \"Studium/1. Semester/Downloads\" and COPY the IMAGE FILE \"usabilityproblemDerWoche3.jpg\" to the FOLDER \"Studium/Tutorium/Einführung MI\""

    # provide task implementation here
    def task_solution(self):
        p = len([p.name for p in Path(self.source_folder).rglob(self.target_file)])
        q = len([p.name for p in Path(self.target_folder).rglob(self.target_file)])

        return p == 1 and q == 1
