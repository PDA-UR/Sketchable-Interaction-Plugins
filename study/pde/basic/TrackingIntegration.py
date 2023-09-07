import os
import queue
import time

from libPySI import PySI

import datetime
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.study.pde.basic.Tip import Tip
from plugins.E import E

from plugins.standard_environment_library.deletion.Deletion import Deletion
from plugins.study.pde.tools.PostIt import PostIt
from plugins.study.pde.tools.VisualLink import VisualLink
from plugins.study.pde.tools.ColorPicker import ColorPicker
from plugins.study.pde.tools.Frame import Frame
from plugins.standard_environment_library.duplicate.Duplicate import Duplicate
from plugins.standard_environment_library.paint_test.Painter import Painter
from plugins.standard_environment_library.paint_test.PainterStrokeSize import PainterStrokeSize
from plugins.standard_environment_library.tag.Tag import Tag
from plugins.standard_environment_library.filesystem.FilesystemAccess import FilesystemAccess
from plugins.standard_environment_library.preview.Preview import Preview

class TrackingIntegration(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ TrackingIntegration __"
    region_display_name = "TrackingIntegration"
    TRACKER_STATE_HOVER = 0
    TRACKER_STATE_DRAG = 1
    UNIX_SOCK_NAME = "/home/vigitia/Desktop/IRPenTracking/uds_test"

    LOG_FILE_FOLDER_PATH = "/home/juergen/Desktop/"
    ELAPSED_START = datetime.datetime.now().timestamp()
    GROUP = 0
    TASK = 0
    LOG_FILE_PATH = LOG_FILE_FOLDER_PATH

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(TrackingIntegration, self).__init__(shape, uuid, "", TrackingIntegration.regiontype, TrackingIntegration.regionname, kwargs)
        TrackingIntegration.GROUP = kwargs["group"]
        TrackingIntegration.TASK = kwargs["task"]

        TrackingIntegration.LOG_FILE_PATH += f"group{TrackingIntegration.GROUP}_task_{TrackingIntegration.TASK}_system_data.csv"
        self.spawned_selectors = False

        print(TrackingIntegration.LOG_FILE_PATH, TrackingIntegration.GROUP, TrackingIntegration.TASK)

        # if not os.path.exists(TrackingIntegration.LOG_FILE_PATH):
        with open(TrackingIntegration.LOG_FILE_PATH, 'w') as out:
            """
            log to file:
                group id
                participant id <=> source of action
                elapsed: time since start
                interaction: system
                active: true or false dependent on whether an action was started or stopped
                action: move, click, dbl_click, etc.
                target: the targeted object of the action
            """
            out.write("group,pid,elapsed,interaction,active,action,target\n")

        # self.add_selectors()

        TrackingIntegration.ELAPSED_START = datetime.datetime.now()
        # pyautogui.keyDown("F5")
        # pyautogui.keyUp("F5")
        #
        # pyautogui.keyDown("F5")
        # pyautogui.keyUp("F5")
        #
        # pyautogui.keyDown("F5")
        # pyautogui.keyUp("F5")
        #
        # pyautogui.keyDown("F5")
        # pyautogui.keyUp("F5")
        #
        # pyautogui.keyDown("F5")
        # pyautogui.keyUp("F5")
        pass

    @SIEffect.on_enter(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid):
        self.add_selectors()

    """
    Delete
    PostIt
    Duplicate
    Link
    ColorPicker
    Painter
    PaintStroke Size
    Tag
    Frame
    FolderAccess
    Image
    Preview
    """
    def add_selectors(self):
        selectors = [Deletion.regionname,
                     PostIt.regionname,
                     Duplicate.regionname,
                     VisualLink.regionname,
                     ColorPicker.regionname,
                     Painter.regionname,
                     PainterStrokeSize.regionname,
                     Tag.regionname,
                     Frame.regionname,
                     FilesystemAccess.regionname,
                     Preview.regionname]

        cw, ch = self.context_dimensions()
        n = len(selectors)

        selector_height = ch // n
        selector_width = selector_height // 2
        offset = (ch - selector_height * n) // 2

        for i in range(n):
            y = offset + i * selector_height
            x1 = offset
            x2 = cw - offset - selector_width

            shape_left = PySI.PointVector([[x1, y], [x1, y + selector_height], [x1 + selector_width, y + selector_height], [x1 + selector_width, y]])
            shape_right = PySI.PointVector([[x2, y], [x2, y + selector_height], [x2 + selector_width, y + selector_height], [x2 + selector_width, y]])

            # self.create_region_via_name(shape_left, selectors[i], True, {"parent": None, "middle": (x1 + selector_width // 2, y + selector_height // 2), "perp_vector": (0, 0)})
            self.create_region_via_name(shape_right, selectors[i], True, {"parent": None, "middle": (x2 + selector_width // 2, y + selector_height // 2), "perp_vector": (0, 0)})
