from libPySI import PySI
from plugins.standard_environment_library.SIEffect import SIEffect
from plugins.standard_environment_library.paint_test.Painter import Painter
from plugins.standard_environment_library.palette.RadialPalette import RadialPalette
from plugins.standard_environment_library.email.InboxItem import InboxItem
from plugins.standard_environment_library.canvas.Clear import Clear
from plugins.standard_environment_library.canvas.Tooltip import Tooltip
from plugins.E import E
import math
from plugins.standard_environment_library.filesystem import Folder, FolderIcon, FolderBubble, TextFile, ImageFile, ZIPFile, PDFFile


class Cursor(SIEffect):
    regiontype = PySI.EffectType.SI_MOUSE_CURSOR
    regionname = PySI.EffectName.SI_STD_NAME_MOUSE_CURSOR
    region_width = E.id.cursor_width / 8
    region_height = E.id.cursor_height / 8

    def __init__(self, shape=PySI.PointVector(), uuid="", kwargs={}):
        super().__init__(shape, uuid, "", Cursor.regiontype, Cursor.regionname, kwargs)

        self.kwargs = kwargs
        self.qml_path = self.set_QML_path(E.id.cursor_qml_path)
        self.color = E.color.cursor_color
        # self.color = PySI.Color(255, 0, 0, 255)
        self.assigned_effect = ""
        self.is_drawing_blocked = False
        self.width = int(Cursor.region_width)
        self.height = int(Cursor.region_height)
        self.visualization_width = 500
        self.visualization_height = 500
        self.with_border = False
        self.clicks = 0
        self.parent_canvas = None
        self.move_target = None
        self.btn_target = None
        self.image_editor_tool = []
        self.image_editor_tooltype = None
        self.has_palette_active = False
        self.palette = None
        self.double_clickables = [Clear.regionname, FolderBubble.FolderBubble.regionname, FolderIcon.FolderIcon.regionname, InboxItem.regionname, ImageFile.ImageFile.regionname, TextFile.TextFile.regionname]
        self.ctrl_pressables = [FolderIcon.FolderIcon.regionname, InboxItem.regionname, ImageFile.ImageFile.regionname, TextFile.TextFile.regionname, ZIPFile.ZIPFile.regionname, PDFFile.PDFFile.regionname]

        self.left_mouse_active = False
        self.right_mouse_active = False
        self.middle_mouse_active = False
        self.double_click_active = False
        self.is_draw_canceled = False
        self.current_effect_texture = ""
        self.current_effect_name = ""
        self.set_QML_data("movement_texture", "res/movement.png", PySI.DataType.STRING)
        self.was_previously_active = False

        self.paint_color = PySI.Color(0, 0, 0, 255)
        self.paint_tool = None
        self.temp = []
        self.ctrl_selected = []
        self.ctrl_pressed = False

        self.tooltip = [r for r in self.current_regions() if r.regionname == Tooltip.regionname][0]
        self.tooltip.update("Hold Left Mouse Button to Show Effects", Tooltip.MOUSE_BUTTON_LEFT)

    @SIEffect.on_link(SIEffect.EMISSION, PySI.LinkingCapability.POSITION)
    def position(self):
        if not self.left_mouse_active:
            for r in self.current_regions():
                if r.regionname == "__SI_SELECTOR_NAME__":
                    r.delete()

        return self.x - self.last_x, self.y - self.last_y, self.x, self.y

    @SIEffect.on_link(SIEffect.RECEPTION, PySI.LinkingCapability.POSITION, PySI.LinkingCapability.POSITION)
    def set_position_from_position(self, rel_x, rel_y, abs_x, abs_y):
        if len(self.present_collisions()) == 1 and self.assigned_effect == "" and not self.left_mouse_active:
            self.tooltip.update("Hold Left Mouse Button to Show Effects", Tooltip.MOUSE_BUTTON_LEFT)
        elif len(self.present_collisions()) == 1 and self.left_mouse_active:
            self.tooltip.update("Choose an Effect", Tooltip.MOUSE_MOVE)
        elif len(self.present_collisions()) == 1 and not self.left_mouse_active:
            self.tooltip.update(f"Hold Right Mouse Button to Draw", Tooltip.MOUSE_BUTTON_RIGHT)
        elif len(self.present_collisions()) > 1 and not self.left_mouse_active:
            self.tooltip.update(f"Hold Left Mouse Button to Move", Tooltip.MOUSE_BUTTON_LEFT)
        elif len(self.present_collisions()) > 1 and self.left_mouse_active and not self.has_palette_active:
            if self.move_target is not None:
                if self.move_target.regionname not in self.double_clickables and self.move_target.regionname not in self.ctrl_pressables:
                    self.tooltip.update("Move Mouse to Move Item", Tooltip.MOUSE_MOVE)
                elif self.move_target.regionname in self.double_clickables or self.move_target.regionname in self.ctrl_pressables:
                    colls = self.move_target.present_collisions_names()

                    if FolderIcon.FolderIcon.regionname not in colls and FolderBubble.FolderBubble.regionname not in colls:
                        self.tooltip.update("Move Mouse to Move Item", Tooltip.MOUSE_MOVE)

    def on_ctrl_pressed(self, is_active):
        self.ctrl_pressed = is_active

    def on_sketch_enter_emit(self, other):
        self.parent_canvas = other
        if self.paint_tool is not None and self.assigned_effect == Painter.regionname:
            self.set_cursor_stroke_width_by_cursorid(self._uuid, self.paint_tool.stroke_width)
            self.set_cursor_stroke_color_by_cursorid(self._uuid, self.paint_tool.color)
        return self.x, self.y, self._uuid

    def on_sketch_continuous_emit(self, other):
        return self.x, self.y, self._uuid

    def on_sketch_leave_emit(self, other):
        self.parent_canvas = None
        kwargs = {}
        if self.paint_tool is not None and self.assigned_effect == Painter.regionname:
            kwargs["color"] = self.paint_tool.color
            kwargs["stroke_width"] = self.paint_tool.stroke_width
            kwargs["__name__"] = Painter.regionname
        return self.x, self.y, self._uuid, self.is_draw_canceled, kwargs

    def on_move_enter_emit(self, other):
        if other.regionname == Painter.regionname and other == self.paint_tool:
            return "", ""

        if self.move_target is None:
            self.move_target = other

        if self.move_target is other:
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_move_continuous_emit(self, other):
        pass

    def on_move_leave_emit(self, other):
        if self.move_target is other:
            self.move_target = None
            return self._uuid, PySI.LinkingCapability.POSITION

        return "", ""

    def on_btn_press_enter_emit(self, other):
        if self.btn_target is None:
            self.btn_target = other

        return self._uuid

    def on_btn_press_continuous_emit(self, other):
        return self._uuid

    def on_btn_press_leave_emit(self, other):
        if self.btn_target is other:
            self.btn_target = None

        return self._uuid

    def on_middle_mouse_click(self, is_active):
        self.middle_mouse_active = is_active

        # if is_active:
        #     if E.capability.cursor_enlarge not in self.cap_emit.keys():
        #         self.enable_effect(E.capability.cursor_enlarge, True, self.on_enlarge_enter_emit, None, None)
        # else:
        #     if E.capability.cursor_enlarge in self.cap_emit.keys():
        #         self.disable_effect(E.capability.cursor_enlarge, True)

        if is_active:
            mc_accepted = False

            fs = [uuid for uuid, name in self.present_collisions() if name == "__ FolderBubble __"]
            fs = [r for r in self.current_regions() if r._uuid in fs]
            fs.sort(key=lambda x: x.parent_level, reverse=True)

            if len(fs) > 0 and not mc_accepted:
                mc_accepted = fs[0].on_middle_click()

    def on_double_click(self, is_active):
        if is_active:
            accecpted = False

            collisions = [uuid for uuid, name in self.present_collisions() if name in self.double_clickables]
            regions = [r for r in self.current_regions() if r._uuid in collisions]

            icons = [r for r in regions if r.regionname == FolderIcon.FolderIcon.regionname]

            if len(icons) > 0 and not accecpted:
                accecpted = icons[0].on_double_clicked()
            else:
                folders = [r for r in regions if r.regionname == FolderBubble.FolderBubble.regionname]
                folders.sort(key=lambda x: x.parent_level, reverse=True)

                if len(folders) > 0 and not accecpted:
                    accecpted = folders[0].on_double_clicked()

            inbox_items = [r for r in regions if r.regionname == InboxItem.regionname]
            textfiles = [r for r in regions if r.regionname == TextFile.TextFile.regionname]
            imagefiles = [r for r in regions if r.regionname == ImageFile.ImageFile.regionname]
            clearbtns = [r for r in regions if r.regionname == Clear.regionname]

            if len(inbox_items) > 0 and not accecpted:
                accecpted = inbox_items[0].on_double_clicked()

            if len(textfiles) > 0 and not accecpted:
                accecpted = textfiles[0].on_double_clicked()

            if len(imagefiles) > 0 and not accecpted:
                accecpted = imagefiles[0].on_double_clicked()

            if len(clearbtns) and not accecpted:
                accecpted = clearbtns[0].on_double_clicked()

    def on_enlarge_enter_emit(self, other):
        pass

    def show_radial_palette(self):
        kwargs = {"source": self}
        self.create_region_via_name(PySI.PointVector([[self.x, self.y], [self.x, self.y + 50], [self.x + 50, self.y + 50], [self.x + 50, self.y]]), RadialPalette.regionname, kwargs=kwargs)

    def remove_radial_palette(self):
        if self.has_palette_active:
            self.has_palette_active = False
            self.palette.remove()
            self.palette = None

    def handle_ctrl_press(self):
        if self.ctrl_pressed:
            collisions = [uuid for uuid, name in self.present_collisions() if name in self.ctrl_pressables]

            if len(collisions) > 0:
                regions = [r for r in self.current_regions() if r._uuid in collisions]
                regions.sort(key=lambda x: x.parent_level, reverse=True)

                for i, r in enumerate(regions):
                    x_offset = len(self.ctrl_selected) * r.width // 8
                    y_offset = len(self.ctrl_selected) * r.height // 8

                    if r not in self.ctrl_selected:
                        r.create_link(self._uuid, PySI.LinkingCapability.POSITION, r._uuid, PySI.LinkingCapability.POSITION)
                        r.is_under_user_control = True
                        r.is_ready = False
                        r.move(self.x - r.absolute_x_pos() - r.width // 2 + r.x + x_offset, self.y - r.absolute_y_pos() - r.height // 4 + r.y + y_offset)
                        self.ctrl_selected.append(r)
                        r.is_blocked = True

        else:
            if len(self.ctrl_selected) > 0:
                for r in self.ctrl_selected:
                    r.remove_link(self._uuid, PySI.LinkingCapability.POSITION, r._uuid, PySI.LinkingCapability.POSITION)
                    r.is_ready = True
                    r.is_under_user_control = False
                    r.is_blocked = False
            self.ctrl_selected.clear()
            self.ctrl_selected = []

    def on_left_mouse_click(self, is_active):
        self.left_mouse_active = is_active
        self.is_draw_canceled = False

        if self.kwargs["draw"] == "RMB":
            if len(self.present_collisions()) == 1 and is_active:
                sorts = [s.is_popup_shown for s in self.current_regions() if s.regionname == "__ FolderSort __"]
                if not any(sorts):
                    self.show_radial_palette()
            else:
                self.remove_radial_palette()
                self.handle_move(is_active)

                self.handle_ctrl_press()

            if self.right_mouse_active: # cancel
                self.is_draw_canceled = True
                if PySI.CollisionCapability.SKETCH in self.cap_emit.keys():
                    self.disable_effect(PySI.CollisionCapability.SKETCH, True)

                if self.parent_canvas is not None:
                    self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))
                self.parent_canvas = None
        elif self.kwargs["draw"] == "LMB":
            self.handle_drawing_click(is_active)

    def handle_drawing_click(self, is_active):
        if is_active:
            if PySI.CollisionCapability.CLICK not in self.cap_emit.keys():
                self.enable_effect(PySI.CollisionCapability.CLICK, True, self.on_btn_press_enter_emit, self.on_btn_press_continuous_emit, self.on_btn_press_leave_emit)

            if self.assigned_effect != "":
                if not self.is_drawing_blocked and PySI.CollisionCapability.SKETCH not in self.cap_emit.keys():
                    self.enable_effect(PySI.CollisionCapability.SKETCH, True, self.on_sketch_enter_emit, self.on_sketch_continuous_emit, self.on_sketch_leave_emit)
        else:
            if PySI.CollisionCapability.SKETCH in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.SKETCH, True)

                if self.parent_canvas is not None:
                    self.parent_canvas.on_sketch_leave_recv(*self.on_sketch_leave_emit(self.parent_canvas))
                self.parent_canvas = None

            if PySI.CollisionCapability.CLICK in self.cap_emit.keys():
                self.disable_effect(PySI.CollisionCapability.CLICK, True)
                if self.btn_target is not None:
                    self.btn_target.on_click_leave_recv(self._uuid)

    def on_right_mouse_click(self, is_active):
        self.right_mouse_active = is_active

        if self.kwargs["draw"] == "RMB":
            self.handle_drawing_click(is_active)
        elif self.kwargs["draw"] == "LMB":
            self.handle_move(is_active)

    def handle_move(self, is_active):
        if is_active:
            if PySI.CollisionCapability.MOVE not in self.cap_emit.keys():
                self.enable_effect(PySI.CollisionCapability.MOVE, True, self.on_move_enter_emit, self.on_move_continuous_emit, self.on_move_leave_emit)
        elif PySI.CollisionCapability.MOVE in self.cap_emit.keys():
            self.disable_effect(PySI.CollisionCapability.MOVE, True)
            if self.move_target is not None:
                if len(self.ctrl_selected) == 0:
                    for i in range(sum([1 for lr in self.move_target.link_relations if lr.sender == self._uuid])):
                        self.move_target.remove_link(self._uuid, PySI.LinkingCapability.POSITION, self.move_target._uuid, PySI.LinkingCapability.POSITION)

                self.move_target.on_move_leave_recv(*self.on_move_leave_emit(self.move_target))

    @SIEffect.on_continuous(PySI.CollisionCapability.ASSIGN, SIEffect.RECEPTION)
    def on_assign_continuous_recv(self, effect_to_assign, effect_display_name, effect_texture, kwargs):
        if self.left_mouse_active:
            if self.assigned_effect != effect_to_assign:
                if self.paint_tool is not None:
                    self.paint_tool.delete()
                self.assigned_effect = effect_to_assign
                self.current_effect_texture = effect_texture
                self.current_effect_name = effect_display_name

                self.set_QML_data("effect_texture", effect_texture, PySI.DataType.STRING)
                self.set_QML_data("effect_text", effect_display_name, PySI.DataType.STRING)
                self.set_QML_data("visible", True, PySI.DataType.BOOL)

                if self.assigned_effect == Painter.regionname:
                    if self.paint_tool is not None:
                        self.paint_tool.delete()

                    shape = []
                    cx, cy = self.absolute_x_pos() + self.width / 2, self.absolute_y_pos() + self.height / 2
                    r = 7

                    for i in range(360):
                        x, y = r * math.cos(i * math.pi / 180) + cx - r, r * math.sin(i * math.pi / 180) + cy - r
                        shape.append([x, y])

                    kwargs["link_partner"] = self
                    kwargs["color"] = self.paint_color
                    self.create_region_via_name(PySI.PointVector(shape), Painter.regionname, kwargs=kwargs)

                self.assign_effect(self.assigned_effect, effect_display_name, effect_texture, kwargs)

    @SIEffect.on_continuous(E.capability.cursor_image_editor_assign, SIEffect.RECEPTION)
    def on_image_editor_assign_continuous_recv(self):
        pass

    @SIEffect.on_enter(PySI.CollisionCapability.HOVER, SIEffect.EMISSION)
    def on_hover_enter_emit(self, other):
        pass

    @SIEffect.on_leave(PySI.CollisionCapability.HOVER, SIEffect.EMISSION)
    def on_hover_leave_emit(self, other):
        pass

    @SIEffect.on_continuous(E.capability.cursor_image_editor_tool_activation, SIEffect.EMISSION)
    def on_tool_activation_continuous_emit(self, other):
        if self.left_mouse_active:
            # self.disable_effect(PySI.CollisionCapability.SKETCH, True)
            self.is_drawing_blocked = True
            return True
        else:
            self.is_drawing_blocked = False

        return False

    @SIEffect.on_leave(E.capability.cursor_image_editor_tool_hiding, SIEffect.RECEPTION)
    def on_hide_tool_leave_recv(self):
        for tool in self.image_editor_tool:
            tool.delete()