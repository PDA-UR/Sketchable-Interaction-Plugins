from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.study.pde.basic.MagnetChoice import MagnetChoice

from plugins.E import E

import math

class Repository(PositionLinkable, Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ Repository __"
    region_display_name = "Repository"

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Repository.regiontype, Repository.regionname, kwargs)
        self.color = PySI.Color(255, 0, 0, 0)
        self.with_border = True
        self.parent = None if "parent" not in kwargs else kwargs["parent"]
        self.parent.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)
        self.parent.repository = self
        cw, ch = self.context_dimensions()

        self.choice_offsetx = 10 * cw / 1920
        self.choice_offsety = 10 * cw / 1080

        colors = list(set(tuple([c.r, c.g, c.b]) for c in self.parent.registered_colors))

        self.choices = [[c[0], c[1], c[2]] for c in colors] + list(set(self.parent.registered_shapes))

        self.create_repository_entries()

    def create_repository_entries(self):
        w = self.width / 8
        h = self.height / 10

        tags_per_row = self.width // (self.choice_offsetx + w)

        for i, choice in enumerate(self.choices):
            x1 = self.absolute_x_pos() + self.choice_offsetx * ((i + 1) % tags_per_row + 1) + w * ((i + 1) % tags_per_row)
            y1 = self.absolute_y_pos() + self.height - h * ((i + 1) // tags_per_row + 1) - self.choice_offsety * ((i + 1) // tags_per_row + 1)

            self.current_height = self.height - h * ((i + 1) // tags_per_row + 1) - self.choice_offsety * ((i + 1) // tags_per_row + 1)
            self.set_QML_data("height", float(self.current_height), PySI.DataType.FLOAT)

            color = PySI.Color(0, 0, 0, 255)
            recognized_shape = ""
            if type(choice) is not str:
                shape = PySI.PointVector([[x1, y1], [x1, y1 + h], [x1 + w, y1 + h], [x1 + w, y1]])
                color = PySI.Color(choice[0], choice[1], choice[2], 255)
            else:
                recognized_shape = choice

                if recognized_shape == "Triangle":
                    tip = [x1 + w / 2, y1]
                    left = [x1, y1 + h]
                    right = [x1 + w, y1 + h]

                    shape = PySI.PointVector([tip, left, right])

                elif recognized_shape == "Rectangle":
                    shape = PySI.PointVector([[x1, y1 + h / 4], [x1, y1 + h / 4 + h / 2], [x1 + w, y1 + h / 4 + h / 2], [x1 + w, y1 + h / 4]])
                elif recognized_shape == "Circle":
                    shape = []
                    for k in range(359, -1, -1):
                        x = x1 + self.choice_offsetx + ((w / 2) * math.cos(k * math.pi / 180))
                        y = y1 + self.choice_offsety + ((w / 2) * math.sin(k * math.pi / 180))

                        shape.append([x, y])

            self.create_region_via_name(shape, MagnetChoice.regionname, False, {"parent": self.parent, "color": color, "recognized_shape": recognized_shape})

    @SIEffect.on_enter("__PARENT_CANVAS__", SIEffect.RECEPTION)
    def on_canvas_enter_recv(self, canvas_uuid: str) -> None:
        pass
