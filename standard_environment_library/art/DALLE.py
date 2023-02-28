from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from dalle2 import Dalle2
import os
import threading
from PIL import Image
from plugins.standard_environment_library.filesystem import ImageFile


class DALLE(Movable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ DALLE __"
    region_display_name = "DALLE"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(DALLE, self).__init__(shape, uuid, "res/openai-avatar.png", DALLE.regiontype, DALLE.regionname, kwargs)
        self.bearer_key = "xAYdkfkzUuGDf9gviaqa1eAbBKJIUIf5OC8VLORa"
        self.qml_path = self.set_QML_path("DALLE.qml")
        self.color = PySI.Color(255, 255, 0, 255)
        self.download_folder = os.getcwd() + "/plugins/standard_environment_library/art/res/temp"
        cw, ch = self.context_dimensions()
        self.icon_width = cw // 22
        self.icon_height = ch // 10
        self.prompts = []
        self.thread = None
        self.img_counter = 0
        self.set_QML_data("is_loading", False, PySI.DataType.BOOL)

        if "DRAWN" in kwargs and kwargs["DRAWN"]:
            self.dalle = Dalle2("sess-" + self.bearer_key)
            x, y = self.aabb[0].x, self.aabb[0].y

            self.shape = PySI.PointVector([[x, y], [x, y + self.icon_height * 2 - 25], [x + 300, y + self.icon_height * 2 - 25], [x + 300, y]])

            self.width = self.get_region_width()
            self.height = self.get_region_height()

            self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
            self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
        pass

    @SIEffect.on_enter("__ON_DALLE_PROMPT__", SIEffect.RECEPTION)
    def on_dalle_prompt_enter(self, prompt):
        self.prompts.append(prompt)

        threading.Thread(target=self.execute_dalle, args=()).start()

    @SIEffect.on_leave("__ON_DALLE_PROMPT__", SIEffect.RECEPTION)
    def on_dalle_prompt_leave(self, prompt):
        self.prompts.remove(prompt)
        threading.Thread(target=self.execute_dalle, args=()).start()

    def execute_dalle(self):
        self.set_QML_data("is_loading", True, PySI.DataType.BOOL)
        filelist = [f for f in os.listdir(self.download_folder)]
        for f in filelist:
            os.remove(os.path.join(self.download_folder, f))

        prompt = " ".join(self.prompts)

        if prompt == " ":
            return

        file_paths = self.dalle.generate_and_download(prompt, self.download_folder)

        for i, fp in enumerate(file_paths):
            self.img_counter += 1
            im = Image.open(fp).convert("RGB")
            im.save(self.download_folder + f"/img{self.img_counter}.png", "png")

            kwargs = {}
            kwargs["path"] = self.download_folder + f"/img{self.img_counter}.png"

            x, y = self.aabb[3].x + self.x, self.aabb[3].y + self.y

            if i == 1:
                x += self.icon_width

            if i == 2:
                y += self.icon_height

            if i == 3:
                x += self.icon_width
                y += self.icon_height

            self.create_region_via_class([[x, y], [x, y + self.icon_height * 2], [x + self.icon_width * 2, y + self.icon_height * 2], [x + self.icon_width * 2, y]], ImageFile, kwargs)

        self.set_QML_data("is_loading", False, PySI.DataType.BOOL)
