from plugins.study.fsm.tasks.__Task import Task
import os


class Task5(Task):
    """
    MOVE all TEXT FILES in FOLDER Downloads into FOLDER Orga

    Although e.g. md files qualify as text files, I focus on txt files to minimize the cognitive load of users.
    I do not evaluate whether users can scan and identify text files based on their suffix.
    I evaluate interaction with the system.
    """
    def __init__(self, participant, repetition):
        super().__init__("5", participant, repetition)

        self.source_folder = "Studium/Downloads"
        self.target_folder = "Studium/Orga"

        self.source_files = [t for t in os.listdir(self.root_path + "/" + self.source_folder) if ".txt" in t]

    #provide task message here
    def task_message(self):
        return "MOVE all TEXT FILES in FOLDER \"Downloads\" into FOLDER \"Orga\"."

    # provide task implementation here
    def task_solution(self):
        target_files = [t for t in os.listdir(self.root_path + "/" + self.target_folder) if ".txt" in t]

        for s in self.source_files:
            if s not in target_files:
                return False

        return not bool(len([t for t in os.listdir(self.root_path + "/" + self.source_folder) if ".txt" in t]))

