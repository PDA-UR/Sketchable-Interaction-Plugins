from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E


class Tag(SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = PySI.EffectName.SI_STD_NAME_PLACEHOLDER
	region_display_name = E.id.tag_display_name

	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		super(Tag, self).__init__(shape, uuid, E.id.tag_texture, Tag.regiontype, Tag.regionname, kwargs)

		self.qml_path = self.set_QML_path(E.id.tag_qml_file_name)
		self.color = E.id.tag_color

		self.enable_effect(E.id.tag_capability_tagging, SIEffect.EMISSION, self.on_tag_enter_emit, None, None)

	def on_tag_enter_emit(self, other):
		text = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)
		return True