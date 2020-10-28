from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.E import E
import time


class Transportable(SIEffect):
    regiontype = PySI.EffectType.SI_CUSTOM_NON_DRAWABLE
    regionname = E.id.transportable_name

    def __init__(self, shape=PySI.PointVector(), uuid="", r="", t="", s="", kwargs={}):
        super(Transportable, self).__init__(shape, uuid, r, t, s, kwargs)
        self.transportation_starttime = None
        self.overall_transportation_length = None
        self.transportation_path = None
        self.transport_ended = False
        self.delta_time = 0
        self.last_time = time.time()
        self.is_clogged = False

    @SIEffect.on_enter(E.id.transportable_capability, SIEffect.RECEPTION)
    def on_transport_enter_recv(self, x, y, length, transportation_path):
        self.delta_time = 0
        self.last_time = time.time()

        if x != self.x and y != self.y:
            self.transportation_starttime = self.last_time
            self.overall_transportation_length = length
            self.transportation_path = transportation_path
            self.move(x - self.relative_x_pos() - self.width / 2, y - self.relative_y_pos() - self.height / 2)

    @SIEffect.on_continuous(E.id.transportable_capability, SIEffect.RECEPTION)
    def on_transport_continuous_recv(self, x, y, has_reached_end):
        t = time.time()
        self.delta_time = t - self.last_time
        self.last_time = t

        if self.is_clogged:
            self.transportation_starttime += self.delta_time
            return

        if x != self.x and y != self.y and not self.transport_ended:
            self.move(x - self.relative_x_pos() - self.width / 2, y - self.relative_y_pos() - self.height / 2)

        if has_reached_end:
            self.transport_ended = True

    @SIEffect.on_leave(E.id.transportable_capability, SIEffect.RECEPTION)
    def on_transport_leave_recv(self):
        self.transport_ended = False
        self.is_clogged = False

    @SIEffect.on_enter(E.id.cb_splitter_evaluate_capability, SIEffect.RECEPTION)
    def on_splitter_evaluate_enter_recv(self, splitter_uuid, x, y):
        if not self.transport_ended:
            self.transport_ended = True
            self.is_clogged = False

            self.move(x, y)

    @SIEffect.on_enter(E.id.cb_merger_evaluate_capability, SIEffect.RECEPTION)
    def on_merger_evaluate_enter_recv(self, merger_uuid, x, y):
        if not self.transport_ended:
            self.transport_ended = True
            self.is_clogged = False

            self.move(x, y)

    @SIEffect.on_enter(E.id.transportable_clogging_capability, SIEffect.EMISSION)
    def on_clogging_state_enter_emit(self, other):
        self.is_clogged = True

    @SIEffect.on_enter(E.id.transportable_clogging_capability, SIEffect.RECEPTION)
    def on_clogging_state_enter_recv(self):
        self.is_clogged = True

    @SIEffect.on_leave(E.id.transportable_clogging_capability, SIEffect.EMISSION)
    def on_clogging_state_leave_emit(self, other):
        self.is_clogged = False

    @SIEffect.on_leave(E.id.transportable_clogging_capability, SIEffect.RECEPTION)
    def on_clogging_state_leave_recv(self):
        self.is_clogged = False
