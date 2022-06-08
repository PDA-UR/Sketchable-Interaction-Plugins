import subprocess
from threading import Thread
import time
import os
import sys


class Task:
    def __init__(self, task, participant, repetition):
        self.task = task
        self.participant = participant
        self.repetition = repetition

        self.root_dir = os.getcwd()

        if sys.platform == "win32":
            self.root_dir = self.root_dir[:self.root_dir.rfind("\\")]
            self.root_dir = self.root_dir + "\\logs"
            self.log_file = self.root_dir + "\\si_data.csv"
        else:
            self.root_dir = self.root_dir[:self.root_dir.rfind("/")]
            self.root_dir = self.root_dir + "/logs"
            self.log_file = self.root_dir + "/si_data.csv"

        if not os.path.exists(self.root_dir):
            os.mkdir(self.root_dir)

        self.start_test_thread()

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as out:
                out.write("pid,system,task,repetition,duration,starttime,endtime\n")

    def start_test_thread(self):
        try:
            t = Thread(target=self.test_thread)
            t.start()
        except:
            print("Start Test Thread failed")

    def test_thread(self):
        proc = subprocess.Popen(["xmessage", "-geometry", "730x200+300+400",
                                 "Bitte lese dir die Aufgabe sorgfaeltig durch. Klicke auf den 'okay' Button, sobald du bereit bist. \n\n Erstelle eine Bubble, die alle Textdateien enthaelt und eine Bubble,\n die alle Bilddateien enthaelt. \n"])
        proc.wait(1000)
        starttime = time.time()

        while True:
            if self.task_solution():
                with open(self.log_file, 'a+') as out:
                    endtime = time.time()
                    duration = endtime - starttime
                    out.write(f"{self.participant},si,{self.task},{self.repetition},{duration},{str(starttime)},{str(endtime)}\n")
                self.finish()
                return
            time.sleep(0.001)

    #override
    def task_solution(self):
        pass

    def finish(self):
        proc = subprocess.Popen(["xmessage","-geometry", "730x200+300+400", "Erfolgreich beendet!"])