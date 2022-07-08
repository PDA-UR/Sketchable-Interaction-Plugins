from plugins.study.fsm.tasks.__Task import Task
import os

# MAYBE REDUNDANT

class Task10(Task):
    """
    FIND an IMAGE FILE with the name usabilityproblemDerWoche3.jpg by NAVIGATING to FOLDER 1. Semester/Einführung MI/Übung
    """
    def __init__(self, participant, repetition):
        super().__init__("10", participant, repetition)

    #provide task message here
    def task_message(self):
        return "FIND an IMAGE FILE with the name usabilityproblemDerWoche3.jpg by NAVIGATING to FOLDER \"1. Semester/Einführung MI/Übung\""

    # provide task implementation here
    def task_solution(self):
        return False