from plugins.study.fsm.tasks.__Task import Task
import os


class Task4(Task):
    """
    MOVE an incoming TEXT FILE from the Desktop to the FOLDER "Orga" and RENAME that TEXTFILE to "rückmeldungWS22.pdf" (appears via conveyer belt)
    """
    def __init__(self, participant, repetition):
        super(Task4, self).__init__("4", participant, repetition)
        self.target_folder = "Orga"
        self.target_file = "rückmeldungWS22.pdf"

    #provide task message here
    def task_message(self):
        return "MOVE an incoming PDF FILE from the Desktop to the FOLDER \"Orga\" and RENAME that TEXTFILE to \"rückmeldungWS22.pdf\"."

    # provide task implementation here
    def task_solution(self):
        return self.target_file in os.listdir(self.root_path + "/" + "Studium/" + self.target_folder)
