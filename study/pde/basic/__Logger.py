import threading

from plugins.study.pde.basic import TrackingIntegration
import datetime

class Logger:
    IS_LOGGING = True

    @staticmethod
    def log(action, tss, tse, tid, target, tracker, with_print=False):
        threading.Thread(target=Logger.__log__, args=(action, tss, tse, tid, target, tracker, with_print)).start()
        # elapsed_start = tss - datetime.datetime.timestamp(TrackingIntegration.TrackingIntegration.ELAPSED_START)
        # elapsed_end = tse - datetime.datetime.timestamp(TrackingIntegration.TrackingIntegration.ELAPSED_START)
        # start = f"{TrackingIntegration.TrackingIntegration.GROUP},{tid},{elapsed_start},system,{True},{action},{target}"
        # end = f"{TrackingIntegration.TrackingIntegration.GROUP},{tid},{elapsed_end},system,{False},{action},{target}"
        #
        # if with_print:
        #     print(start)
        #     print(end)
        #
        # if Logger.IS_LOGGING:
        #         threading.Thread(target=Logger.__write_to_file, args=(start, end, tracker.LOG_FILE_PATH)).start()

    @staticmethod
    def __log__(action, tss, tse, tid, target, tracker, with_print):
        elapsed_start = tss - TrackingIntegration.TrackingIntegration.ELAPSED_START
        elapsed_end = tse - TrackingIntegration.TrackingIntegration.ELAPSED_START
        start = f"{tracker.GROUP},{tid},{elapsed_start},system,{True},{action},{target}"
        end = f"{tracker.GROUP},{tid},{elapsed_end},system,{False},{action},{target}"

        if with_print:
            print(start)
            print(end)

        if Logger.IS_LOGGING:
            Logger.__write_to_file(start, end, tracker.LOG_FILE_PATH)

    @staticmethod
    def __write_to_file(start, end, file_path):
        with open(file_path, "a") as out:
            print(start, file=out)
            print(end, file=out)