from plugins.study.fsm.tasks.__Task import Task
import os


class Task1(Task):
    """
    CREATE an empty TEXT FILE in FOLDER "Studium" and NAME that TEXT FILE "notizen.txt".
    """
    def __init__(self, participant, repetition):
        super().__init__("1", participant, repetition)
        self.target_file = "notizen.txt"
        self.target_folder = "Studium"

    #provide task message here
    def task_message(self):
        return "CREATE an empty TEXT FILE in FOLDER \"Studium\" and NAME that TEXT FILE \"notizen.txt\"."

    # provide task implementation here
    def task_solution(self):
        return self.target_file in os.listdir(self.root_path + "/" + self.target_folder)