from plugins.study.fsm.tasks.__Task import Task
import os
from pathlib import Path


class Task12(Task):
    """
    FIND a TEXT FILE named übungssitzung3.md by NAVIGATING to a FOLDER from FOLDER”Studium/Tutorium”, EDIT the file übungssitzung3.md by adding the line ”* es wurden wenig Fragen gestellt.”, and RENAME übungssitzung3.md to notizenÜbungssitzung3.md
    """
    def __init__(self, participant, repetition):
        super().__init__("12", participant, repetition)
        self.source_folder = self.root_path + "/Studium/Tutorium/Einführung MI/Übung"
        self.target_content = "* es wurden wenig Fragen gestellt."

    #provide task message here
    def task_message(self):
        return "FIND a TEXT FILE named \"übungssitzung3.md\" by NAVIGATING to FOLDER \"Tutorium/Einführung MI/Übung\", EDIT the file \"übungssitzung3.md\ by adding the line ”* es wurden wenig Fragen gestellt.”, and RENAME \"übungssitzung3.md\" to \"notizenÜbungssitzung3.md\""

    # provide task implementation here
    def task_solution(self):
        if len([p.name for p in Path(self.source_folder).rglob("übungssitzung3.md")]) != 0:
            return False

        if len([p.name for p in Path(self.source_folder).rglob("notizenÜbungssitzung3.md")]) != 1:
            return False

        line = ""
        with open(self.source_folder + "/notizenÜbungssitzung3.md") as file:
            lines = file.readlines()

            if len(lines) > 0:
                line = lines[0]

        return line == self.target_content
