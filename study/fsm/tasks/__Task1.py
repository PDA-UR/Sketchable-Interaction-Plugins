from plugins.study.fsm.tasks.__Task import Task


class Task1(Task):
    def __init__(self, participant, repetition):
        super().__init__("1", participant, repetition)

    def task_solution(self):
        return False