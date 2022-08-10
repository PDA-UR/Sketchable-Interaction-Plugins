from libPySI import PySI

from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.PositionLinkable import PositionLinkable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.E import E
from plugins.standard_environment_library.filesystem.FilesystemEntry import FilesystemEntry
import os


class InteractionPriorization(PositionLinkable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ InteractionPriorization __"
    region_display_name = "InteractionPriorization"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(InteractionPriorization, self).__init__(shape, uuid, "", InteractionPriorization.regiontype, InteractionPriorization.regionname, kwargs)
        self.color = PySI.Color(255, 255, 0, 255)
        self.with_border = False
        self.parent = kwargs["parent"]
        self.parent.prio = self
        self.folder_path = ""
        self.folder_regionname = ""
        self.create_link(self.parent._uuid, PySI.LinkingCapability.POSITION, self._uuid, PySI.LinkingCapability.POSITION)

    @SIEffect.on_continuous("ADD_TO_FOLDERBUBBLE", SIEffect.RECEPTION)
    def on_add_to_folder_continuous_recv(self):
        if self.parent.is_under_user_control:
            collisions = [uuid for uuid, name in self.present_collisions()]
            if len(collisions) > 0:
                regions = [r for r in self.current_regions() if r._uuid in collisions]
                regions = [r for r in regions if hasattr(r, "parent_level") and r.parent_level == max(regions, key=lambda x: x.parent_level).parent_level]
                self.folder_path = regions[0].path
                self.folder_regionname = regions[0].regionname

    @SIEffect.on_continuous("ADD_TO_FOLDERICON", SIEffect.RECEPTION)
    def on_add_to_foldericon_continuous_recv(self):
        if self.parent.is_under_user_control:
            collisions = [uuid for uuid, name in self.present_collisions()]
            if len(collisions) > 0:
                regions = [r for r in self.current_regions() if r._uuid in collisions]
                regions = [r for r in regions if hasattr(r, "parent_level") and r.parent_level == max(regions, key=lambda x: x.parent_level).parent_level]
                self.folder_path = regions[0].path
                self.folder_regionname = regions[0].regionname