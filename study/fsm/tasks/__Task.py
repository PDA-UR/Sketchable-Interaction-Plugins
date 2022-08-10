import subprocess
from threading import Thread
import time
import os
import sys
from plugins.standard_environment_library.filesystem.FilesystemAccess import FilesystemAccess
import shutil
from datetime import datetime
import codecs


class Task:
    def __init__(self, task, participant, repetition):
        self.task = task
        self.participant = participant
        self.repetition = repetition

        self.root_dir = os.getcwd()
        self.root_path = FilesystemAccess.root_path

        self.root_dir = self.root_dir[:self.root_dir.rfind("/")]
        self.root_dir = self.root_dir + "/logs"
        self.log_file = self.root_dir + "/si_data.csv"
        self.w, self.h, self.x, self.y = 730 * 2, 200 * 2, 300, 400


        if not os.path.exists(self.root_dir):
            os.mkdir(self.root_dir)

        self.start_test_thread()

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as out:
                out.write("pid,system,task,repetition,duration,starttime,endtime\n")
        else:
            self.backup()

    def backup(self):
        if not os.path.isdir(self.root_dir + "/backup"):
            os.mkdir(self.root_dir + "/backup")

        shutil.copy(self.log_file, self.root_dir + "/backup/si_data" + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + ".csv")

    def start_test_thread(self):
        try:
            t = Thread(target=self.test_thread)
            t.start()
        except:
            print("Start Test Thread failed")

    def test_thread(self):
        intro = "Bitte lese dir die Aufgabe sorgfältig durch. Klicke auf den 'OK' Button unten rechts im Fenster, sobald du bereit bist. \n\n"
        proc = subprocess.Popen(["gxmessage", "-geometry", f"{self.w}x{self.h}+{self.x}+{self.y}",
                                 intro + self.task_message()])
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
            time.sleep(0.016)

    #override
    def task_solution(self):
        pass
    #override
    def task_message(self):
        return ""

    def finish(self):
        proc = subprocess.Popen(["gxmessage","-geometry", f"{self.w}x{self.h}+{self.x}+{self.y}", "Erfolgreich beendet!"])