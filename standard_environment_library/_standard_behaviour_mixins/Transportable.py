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
        self.mergers = []

    @SIEffect.on_enter(E.capability.transportable_transportable, SIEffect.RECEPTION)
    def on_transport_enter_recv(self, x, y, length, transportation_path):
        self.delta_time = 0
        self.last_time = time.time()
        self.transportation_starttime = self.last_time
        self.overall_transportation_length = length
        self.transportation_path = transportation_path
        self.transport_ended = False

    @SIEffect.on_continuous(E.capability.transportable_transportable, SIEffect.RECEPTION)
    def on_transport_continuous_recv(self, x, y, has_reached_end, moves_first_when_clogged):
        t = time.time()
        self.delta_time = t - self.last_time
        self.last_time = t

        if self.is_clogged and not moves_first_when_clogged:
            self.transportation_starttime += self.delta_time
        else:
            if x != self.x and y != self.y and not self.transport_ended:
                new_x = (x - self.absolute_x_pos()) + self.x - self.width / 2
                new_y = (y - self.absolute_y_pos()) + self.y - self.height / 2

                self.move(new_x, new_y)

            if has_reached_end:
                self.transport_ended = True

    @SIEffect.on_leave(E.capability.transportable_transportable, SIEffect.RECEPTION)
    def on_transport_leave_recv(self):
        self.transport_ended = False
        self.is_clogged = False

    @SIEffect.on_enter(E.capability.cb_splitter_evaluate, SIEffect.RECEPTION)
    def on_splitter_evaluate_enter_recv(self, splitter_uuid, x, y):
        if not self.transport_ended:
            self.transport_ended = True
            self.move(x, y)

    @SIEffect.on_enter(E.capability.cb_merger_evaluate, SIEffect.RECEPTION)
    def on_merger_evaluate_enter_recv(self, merger_uuid, x, y):
        # if not self.transport_ended and not self.is_under_user_control:
            # if merger_uuid not in self.mergers:
            #     self.mergers.append(merger_uuid)
        self.move(x, y)

    @SIEffect.on_leave(E.capability.cb_merger_evaluate, SIEffect.RECEPTION)
    def on_merger_evaluate_leave_recv(self, merger_uuid):
        # if merger_uuid in self.mergers:
        #     del self.mergers[self.mergers.index(merger_uuid)]
        pass

    # clogging is broken and breaks CBs
    @SIEffect.on_enter(E.capability.transportable_clogging, SIEffect.EMISSION)
    def on_clogging_state_enter_emit(self, other):
        self.is_clogged = False

    @SIEffect.on_enter(E.capability.transportable_clogging, SIEffect.RECEPTION)
    def on_clogging_state_enter_recv(self):
        self.is_clogged = False

    @SIEffect.on_leave(E.capability.transportable_clogging, SIEffect.EMISSION)
    def on_clogging_state_leave_emit(self, other):
        self.is_clogged = False

    @SIEffect.on_leave(E.capability.transportable_clogging, SIEffect.RECEPTION)
    def on_clogging_state_leave_recv(self):
        self.is_clogged = False
