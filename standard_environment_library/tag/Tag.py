from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.E import E


class Tag(Deletable, Movable, SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = E.id.tag_name
	region_display_name = E.id.tag_display_name

	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		Deletable.__init__(self, shape, uuid, E.id.tag_texture, Tag.regiontype, Tag.regionname, kwargs)
		Movable.__init__(self, shape, uuid, E.id.tag_texture, Tag.regiontype, Tag.regionname, kwargs)
		SIEffect.__init__(self, shape, uuid, E.id.tag_texture, Tag.regiontype, Tag.regionname, kwargs)

		self.qml_path = self.set_QML_path(E.id.tag_qml_file_name)
		self.color = E.id.tag_color
		self.text = "Hello World"

	@SIEffect.on_enter(E.id.tag_capability_tagging, SIEffect.EMISSION)
	def on_tag_enter_emit(self, other):
		text = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)
		self.text = text
		return True