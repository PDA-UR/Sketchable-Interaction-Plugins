from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library._standard_behaviour_mixins.UnRedoable import UnRedoable
from plugins.standard_environment_library._standard_behaviour_mixins.Rotateable import Rotateable
from plugins.E import E


class Tag(Deletable, Movable, SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = E.id.tag_name
	region_display_name = E.id.tag_display_name

	# @UnRedoable.action
	# @Deletable.unredoable
	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		super().__init__(shape, uuid, E.id.tag_texture, Tag.regiontype, Tag.regionname, kwargs)

		self.qml_path = self.set_QML_path(E.id.tag_qml_file_name)
		self.color = E.color.tag_color
		self.text = "Hello World"
		self.text_enterable_id = -1

	# @UnRedoable.action
	@SIEffect.on_enter(E.capability.tag_tagging, SIEffect.EMISSION)
	def on_tag_enter_emit(self, other):
		text = self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)

	@SIEffect.on_enter("__ON_TAGGING__", SIEffect.EMISSION)
	def on_tagging_enter_emit(self, other):
		return self.color, self.get_QML_data(E.id.tag_text_from_qml, PySI.DataType.STRING)

	@SIEffect.on_continuous("__RECOLOR__", SIEffect.RECEPTION)
	def on_recolor_continuous_recv(self, r, g, b):
		self.color = PySI.Color(r, g, b, 255)

	# @SIEffect.on_enter("__ TEXT __ ", SIEffect.RECEPTION)
	# def on_text_enter_emit(self, _id):
	# 	self.text_enterable_id = _id
	#
	# @SIEffect.on_leave("__ TEXT __ ", SIEffect.RECEPTION)
	# def on_text_leave_recv(self):
	# 	pass