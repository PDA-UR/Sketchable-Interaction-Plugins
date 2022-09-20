from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
import cmath
import math
from shapely import geometry
import threading


class RadialPalette(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = "__ RadialPalette __"
    region_display_name = "RadialPalette"

    def __init__(self, shape: PySI.PointVector = PySI.PointVector(), uuid: str = "", kwargs: dict = {}) -> None:
        super(RadialPalette, self).__init__(shape, uuid, "", RadialPalette.regiontype, RadialPalette.regionname, kwargs)
        self.cursor_source = kwargs["source"]
        self.cursor_source.has_palette_active = True
        self.cursor_source.palette = self
        self.as_selector = True
        self.radius = 300
        self.selectors = []
        self.available_plugins = self.available_plugins()
        excluded_plugins = self.excluded_plugins()
        for ep in excluded_plugins:
            if ep in self.available_plugins:
                self.available_plugins.remove(ep)
        self.with_border = False
        self.color = PySI.Color(0, 0, 0, 0)

    @SIEffect.on_continuous(E.capability.canvas_parent, SIEffect.RECEPTION)
    def on_canvas_continuous_emit(self, canvas_uuid):
        if len(self.selectors) == 0:
            self.spawn_selectors()

    def normalized_vector(self, v):
        n = float(self.vector_length(v))

        if n != 0:
            return [float(v[i]) / n for i in range(len(v))]
        else:
            return [-1 for i in range(len(v))]

    def vector_length(self, v):
        return math.sqrt(self.vector_dot(v, v))

    def vector_dot(self, u, v):
        return sum((a * b) for a, b in zip(u, v))

    def perpendicular_vector(self, v):
        return -v[1], v[0]

    def calculate_radial_segmentation(self, n, r, x, y):
        for i in range(n):
            rr = cmath.rect(r, (2 * cmath.pi) * (i / n))
            yield [round(x + rr.real, 2), round(y + rr.imag, 2)]


    def calculate_inner_segmentation_coordinates(self, coords, cx, cy):
        lx, ly = coords[0]
        rx, ry = coords[1]
        normalized_rl = self.normalized_vector((rx - lx, ry - ly))
        outer_len = self.vector_length((rx - lx, ry - ly))
        svx, svy = lx + normalized_rl[0] * (outer_len * 0.5), ly + normalized_rl[1] * (outer_len * 0.5)
        perpendicular_rl = self.normalized_vector((cx - svx, cy - svy))
        outer_len -= outer_len * 0.92
        lx = lx + normalized_rl[0] * outer_len
        ly = ly + normalized_rl[1] * outer_len
        rx = rx - normalized_rl[0] * outer_len
        ry = ry - normalized_rl[1] * outer_len
        lenl = self.vector_length((cx - lx, cy - ly))
        lenr = self.vector_length((cx - rx, cy - ry))
        lenl -= lenl * 0.2
        lenr -= lenr * 0.2
        normalized_l = self.normalized_vector([cx - lx, cy - ly])
        normalized_r = self.normalized_vector([cx - rx, cy - ry])
        nlx, nly = lx + normalized_l[0] * lenl + normalized_rl[0] * outer_len, ly + normalized_l[1] * lenl + normalized_rl[1] * outer_len
        nrx, nry = rx + normalized_r[0] * lenr - normalized_rl[0] * outer_len, ry + normalized_r[1] * lenr - normalized_rl[1] * outer_len

        return self.round_edge([[lx, ly], [nlx, nly], [nrx, nry], [rx, ry]]), (svx, svy), perpendicular_rl

    def spawn_selectors(self):
        cx, cy = self.aabb[0].x, self.aabb[0].y
        coords = list(self.calculate_radial_segmentation(len(self.available_plugins), self.radius, cx, cy))
        for i in range(1, len(coords) + 1):
            l, r = coords[i - 1], coords[i % len(self.available_plugins)]
            shape, middle, perp_vector = self.calculate_inner_segmentation_coordinates((l, r), cx, cy)
            self.create_region_via_name(PySI.PointVector(shape), self.available_plugins[i - 1], self.as_selector, {"parent": self, "middle": middle, "perp_vector": perp_vector})
            # threading.Thread(target=lambda: self.create_region_via_name(PySI.PointVector(shape), self.available_plugins[i - 1], self.as_selector, {"parent": self, "middle": middle, "perp_vector": perp_vector})).start()

    def remove(self):
        for s in self.selectors:
            s.delete()
        self.delete()

    def round_edge(self, pts):
        return [[t[0], t[1]] for t in list(geometry.Polygon(pts).buffer(10, single_sided=True, join_style=geometry.JOIN_STYLE.round, cap_style=geometry.CAP_STYLE.round).exterior.coords)]
