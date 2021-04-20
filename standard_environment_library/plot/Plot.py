from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
from plugins.standard_environment_library._standard_behaviour_mixins.Movable import Movable
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable

import matplotlib
matplotlib.use('Agg')  # required
import matplotlib.pyplot as plt
import numpy as np
np.seterr(divide='ignore', invalid='ignore')  # optional for quenching annoying warnings


class Plot(Deletable, Movable, SIEffect):
	regiontype = PySI.EffectType.SI_CUSTOM
	regionname = E.id.plot_name
	region_display_name = E.id.plot_display_name

	def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
		super(Plot, self).__init__(shape, uuid, E.id.plot_texture, Plot.regiontype, Plot.regionname, kwargs)

		self.qml_path = self.set_QML_path(E.id.plot_qml_file_name)
		self.color = E.id.plot_color

		# rework this into a linking action reception function or collision event reception function
		figure = plt.figure()
		plot = figure.add_subplot(111)

		# draw a cardinal sine plot
		x = np.arange(0, 100, 0.1)
		y = np.sin(x) / x
		plot.plot(x, y)

		self.show(figure)

	def show(self, figure):
		np_fig = self.fig_2_ndarray(figure)
		self.width, self.height, _ = np_fig.shape

		x = self.relative_x_pos()
		y = self.relative_y_pos()

		self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])

		self.set_QML_data("image", np_fig.tobytes(), PySI.DataType.IMAGE_AS_BYTES, {"width": self.width, "height": self.height})
		self.set_QML_data("img_width", self.width, PySI.DataType.INT)
		self.set_QML_data("img_height", self.height, PySI.DataType.INT)
		self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
		self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

	def hide(self):
		self.set_QML_data("image", None, PySI.DataType.IMAGE_AS_BYTES, {"width": self.width, "height": self.height})

		x = self.relative_x_pos()
		y = self.relative_y_pos()

		self.width, self.height = 200, 200

		self.shape = PySI.PointVector([[x, y], [x, y + self.height], [x + self.width, y + self.height], [x + self.width, y]])

		self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
		self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)

	def fig_2_ndarray(self, fig, mode="rgba"):
		fig.canvas.draw()

		# Get the RGBA buffer from the figure
		w, h = fig.canvas.get_width_height()
		buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
		buf.shape = (w, h, 4)

		if mode == "rgba":
			# canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
			buf = np.roll(buf, 3, axis=2)
			return buf
		elif mode == "argb":
			pass
