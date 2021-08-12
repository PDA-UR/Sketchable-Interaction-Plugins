from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library._standard_behaviour_mixins.Deletable import Deletable
from plugins.standard_environment_library.tangible.camera.ArUcoMarker import ArUcoMarker

class ScanCameraAreaDetection(Deletable, SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ ScanCameraAreaDetection __"

    def __init__(self, shape: PySI.PointVector=PySI.PointVector(), uuid: str="", kwargs: dict={}) -> None:
        super(ScanCameraAreaDetection, self).__init__(shape, uuid, "res/0.png", ScanCameraAreaDetection.regiontype, ScanCameraAreaDetection.regionname, kwargs)
        self.source = "libStdSI"
        self.color = PySI.Color(255, 255, 255, 255)

        w, h = self.context_dimensions()
        rows, cols = self.marker_distribution(w, h)
        self.add_markers(rows, cols, w / cols)

    def marker_distribution(self, w: int, h: int, min: int=10, max: int=20) -> tuple:
        # + [k for k in range(min, max)]
        return [(int(h / (w / i)), int(i)) for i in [48] if w % i == 0 and h % (w / i) == 0][-1]

    def add_markers(self, rows: int, cols: int, marker_size: int, offset: int=15) -> None:
        for i in range(rows):
            y = i * marker_size + offset
            y2 = y + marker_size - (offset << 1)

            for k in range(cols):
                x = k * marker_size + offset
                x2 = x + marker_size - (offset << 1)

                self.create_region_via_name(PySI.PointVector([[x, y], [x, y2], [x2, y2], [x2, y]]), ArUcoMarker.regionname, False, {"texture": f"res/{cols * i + k}.png"})
