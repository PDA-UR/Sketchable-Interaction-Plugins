import sys

from libPySI import PySI
import inspect
import os

## @package SIEffect
# Documentation for this module / class
#
# Used as central entry point for all SIGRun plugins

## Super Class from which all subsequent plugins are derived
#
# This Class itself is derived from PySI written in C++ which is documented separately within SIGRun
class SIEffect(PySI.Effect):
    ## member constant to mark an effect or link emittable
    EMISSION = True

    ## static member attribute to mark an effect or link receivable
    RECEPTION = False

    ## static member attribute to signal that it's associated effect does not display an icon (texture) when drawn as a region
    TEXTURE_PATH_NONE = ""

    ## static member attribute to notify SIGRun to resample a region's shape when changed from PySI
    RESAMPLING = True

    ## static member attribute to notify SIGRun to not resample a region's shape when changed from PySI
    # Use with caution!
    # May lead to unexpected / barely debuggable behaviour!
    NO_RESAMPLING = False

    ## Decorator for registering on_enter collision events
    #
    # Decorates a specific function in other plugin files to be used as an on_enter collision event.
    # Recommended use: @SIEffect.on_enter(<capability>, <transmission_type>)
    #
    # This decorator adds no functionality and only provides easier syntax for defining on_enter collision events.
    # The decorator is detected by the SIGRun plugin transpiler during the plugin loading step.
    # In this step, the transpiler removes the decorator and appends an equivalent function call to the plugin's constructor, in order to register the on_enter collision event.
    #
    # @param capability the str value serving as the identifier for the on_enter collision event
    # @param transmission_type the bool value serving to determine whether the event shall be emitted (SIEffect.EMISSION) or received (SIEffect.RECEPTION)
    #
    # @return the decorated function
    @staticmethod
    def on_enter(capability, transmission_type):
        def wrap(f):
            def wrapped_f(*args):
                return f(*args)
            return wrapped_f
        return wrap

    ## Decorator for registering on_continuous collision events
    #
    # Decorates a specific function in other plugin files to be used as an on_continuous collision event.
    # Recommended use: @SIEffect.on_continuous(<capability>, <transmission_type>)
    #
    # This decorator adds no functionality and only provides easier syntax for defining on_continuous collision events.
    # The decorator is detected by the SIGRun plugin transpiler during the plugin loading step.
    # In this step, the transpiler removes the decorator and appends an equivalent function call to the plugin's constructor, in order to register the on_continuous collision event.
    #
    # @param capability the str value serving as the identifier for the on_continuous collision event
    # @param transmission_type the bool value serving to determine whether the event shall be emitted (SIEffect.EMISSION) or received (SIEffect.RECEPTION)
    #
    # @return the decorated function
    @staticmethod
    def on_continuous(capability, transmission_type):
        def wrap(f):
            def wrapped_f(*args):
                return f(*args)
            return wrapped_f
        return wrap

    ## Decorator for registering on_leave collision events
    #
    # Decorates a specific function in other plugin files to be used as an on_leave collision event.
    # Recommended use: @SIEffect.on_leave(<capability>, <transmission_type>)
    #
    # This decorator adds no functionality and only provides easier syntax for defining on_leave collision events.
    # The decorator is detected by the SIGRun plugin transpiler during the plugin loading step.
    # In this step, the transpiler removes the decorator and appends an equivalent function call to the plugin's constructor, in order to register the on_leave collision event.
    #
    # @param capability the str value serving as the identifier for the on_leave collision event
    # @param transmission_type the bool value serving to determine whether the event shall be emitted (SIEffect.EMISSION) or received (SIEffect.RECEPTION)
    #
    # @return the decorated function
    @staticmethod
    def on_leave(capability, transmission_type):
        def wrap(f):
            def wrapped_f(*args):
                return f(*args)
            return wrapped_f
        return wrap

    ## Decorator for registering linking actions
    #
    # Decorates a specific function in other plugin files to be used as an linking action.
    # Recommended use: @SIEffect.on_link(<transmission_type>, <emission_capability>, <reception_capability>)
    #
    # This decorator adds no functionality and only provides easier syntax for defining linking actions.
    # The decorator is detected by the SIGRun plugin transpiler during the plugin loading step.
    # In this step, the transpiler removes the decorator and appends an equivalent function call to the plugin's constructor, in order to register the linking action.
    # Here, the transpiler differentiates the emission of a linking action: @SIEffect.on_link(SIEffect.EMISSION, <capability>)
    # and the reception of a linking action: @SIEffect.on_link(SIEffect.Reception, <emission_capability>, <reception_capability>)
    #
    # @param transmission_type the bool value serving to determine whether the event shall be emitted (SIEffect.EMISSION) or received (SIEffect.RECEPTION)
    # @param emission_capability the str value serving as the identifier of with which the linking action was emitted from its source
    # @param reception_capability the str value serving as the identifier of with which the linking action shall be received
    #
    # @return the decorated function
    @staticmethod
    def on_link(transmission_type, emission_capability, reception_capability=None):
        def wrap(f):
            def wrapped_f(*args):
                return f(*args)
            return wrapped_f
        return wrap

    ## constructor
    #
    # Constructs a new SIEffect object based on the given arguments.
    #
    # @param self the object pointer
    # @param shape the contour of the drawn region (PySI.PointVector)
    # @param aabb the axis-aligned bounding-box of the drawn region (PySI.PointVector)
    # @param uuid the universally unique identifier of the drawn region (str)
    # @param texture_path the path to an image intended to be used as an icon for the drawn region (str)
    # @param kwargs keyworded arguments which may necessary for more specific implementations of region effects (dict)
    # @param __source__ the source of the plugin e.g. standard environment library (str)
    #
    # @return None
    def __init__(self, shape: PySI.PointVector, uuid: str, texture_path: str, regiontype: int, regionname: str, kwargs: dict, __source__: str="custom") -> None:
        super().__init__(shape, uuid, texture_path, kwargs)

        ## member attribute variable serving as a rendering hint for showing a regions border
        self.with_border = True

        tmp = sys.modules[self.__class__.__module__].__file__
        texture_path = tmp[0:tmp.rindex("/") + 1] + texture_path

        ## member attribute variable containing the shape (contour) of a drawn region as a PySI.PointVector
        self.shape = shape

        ## member attribute variable containing the axis-aligned bounding-box (aabb) of a drawn region as a PySI.PointVector
        #
        # This variable is automatically computed when shape is changed.
        # It is recommended to use this variable read-only.
        self.aabb

        ## member variable containing the maximum width of the region
        #
        # computed via aabb

        self.width = self.get_region_width()

        ## member variable containing the maximum height of the region
        #
        # computed via aabb
        self.height = self.get_region_height()

        ## member attribute variable containing the universally unique identifier (uuid) of a drawn region as a str
        self._uuid = uuid

        ## member attribute variable containing the name of a drawn region as a str
        self.name = regionname

        ## member attribute variable containing the type of effect of a drawn region as a PySI.EffectType
        #
        # Effect implementation which are currently not part of the Standard Environment Library of SIGRun are required to be of type SI_CUSTOM
        self.region_type = regiontype

        ## member attribute variable containing the source of effect of a drawn region as a str
        #
        # Effect implementation which are currently not part of the Standard Environment Library of SIGRun are encouraged to not start with "libStdSI"
        self.source = "libStdSI"

        ## member attribute variable containing the path to a QML file for styling of a drawn region as a str
        #
        # This value can be left empty if no visualization of the region is intended (e.g. Container-Regions for External Applications or MouseCursor)
        # @see Container
        # @see MouseCursor
        self.qml_path = ""

        ## member attribute variable containing the last relative movement of the region according to the x axis as a float
        self.delta_x = 0

        ## member attribute variable containing the last relative movement of the region according to the y axis as a float
        self.delta_y = 0

        ## member attribute variable containing the last absolute x coordinate as a float
        self.last_x = 0

        ## member attribute variable containing the last absolute y coordinate as a float
        self.last_y = 0

        ## member attribute variable containing the fill color of a region in RGBA as a PySI.Color
        self.color = PySI.Color(33, 33, 33, 127)

        ## member attribute variable which is true when an user directly controls the region (e.g. moving it around) as a bool
        self.is_under_user_control = False

        ## member attribute variable storing the uuids of present cursors once a region drawing is to be registered as a PySI.StringVector
        self.__registered_regions__ = PySI.StringVector()

        ## member attribute variable storing the path to the image file used as texture for a region
        self.texture_path = texture_path

        if self.texture_path != "":
            ## member attribute variable storing the width of a texture of a region drawing as a float
            #
            # This value is only set if texture_path is a valid path
            self.texture_width = 75

            ## member attribute variable storing the height of a texture of a region drawing as a float
            #
            # This value is only set if texture_path is a valid path
            self.texture_height = 75

            # apply data in QML
            self.set_QML_data("img_width", self.texture_width, PySI.DataType.INT)
            self.set_QML_data("img_height", self.texture_height, PySI.DataType.INT)
            self.set_QML_data("img_path", self.texture_path, PySI.DataType.STRING)
            self.set_QML_data("widget_width", self.width, PySI.DataType.FLOAT)
            self.set_QML_data("widget_height", self.height, PySI.DataType.FLOAT)
            self.set_QML_data("uuid", self._uuid, PySI.DataType.STRING)

        ## member attribute variable storing keys to functions which are called when collision events occur for emitting data to receiving regions
        #
        # This variable is a PySI.String2_String2FunctionMap_Map (c++-bindings) and uses capabilities (str) as keys to the inner String2FunctionMap.
        # The inner String2FunctionMap uses collision event names (PySI.ON_ENTER ("on_enter"), PySI:ON_CONTINUOUS ("on_continuous"), PySI.ON_LEAVE ("on_leave")) as keys to their corresponding functions as values
        #
        # Example:
        #
        # self.cap_emit["CAPABILITY"] = {PySI.ON_ENTER: self.<function_enter>, PySI:ON_CONTINUOUS: self.<function_continuous>, PySI.ON_LEAVE: self.<function_leave>
        #
        # Therefore, this example allows a region to emit an effect of CAPABILITY once a collision event occurred
        self.cap_emit = PySI.String2String2FunctionMapMap()

        ## member attribute variable storing keys to functions which are called when collision events occur for receiving data from emitting regions
        #
        # This variable is a PySI.String2_String2FunctionMap_Map (c++-bindings) and uses capabilities (str) as keys to the inner String2FunctionMap.
        # The inner String2FunctionMap uses collision event names (PySI.ON_ENTER ("on_enter"), PySI:ON_CONTINUOUS ("on_continuous"), PySI.ON_LEAVE ("on_leave")) as keys to their corresponding functions as values
        #
        # Example:
        #
        # self.cap_recv["CAPABILITY"] = {PySI.ON_ENTER: self.<function_enter>, PySI:ON_CONTINUOUS: self.<function_continuous>, PySI.ON_LEAVE: self.<function_leave>
        #
        # Therefore, this example allows a region to receive an effect of CAPABILITY once a collision event occurred
        self.cap_recv = PySI.String2String2FunctionMapMap()

        ## member attribute variable storing keys to functions which are called when linking events occur for emitting data to receiving regions
        #
        # This variable is a String2FunctionMap (c++-bindings) containing capabilities (str) as keys and functions as values
        #
        # Example with SI-integrated linking of positions for emission case:
        # self.cap_link_emit[PySI.POSITION] = self.<function_position_emit>
        # Therefore, this example emits the positional data of the region to a linked region.

        # Example with custom capability for linking:
        # self.cap_link_emit[<name of capability>] = self.<corresponding function>
        # Therefore, this example emits some data of the region to a linked region based on the capability
        self.cap_link_emit = PySI.String2FunctionMap()

        ## member attribute variable storing keys to functions which are called when linking events occur for emitting data to receiving regions
        #
        # This variable is a PySI.String2_String2FunctionMap_Map (c++-bindings) and uses linking event capability names (str) as keys to the inner String2FunctionMap.
        # The inner String2FunctionMap uses linking event capability names (PySI.POSITION, <own name as str>) as keys to their corresponding functions as values.
        # The outer key corresponds to the emission capability.
        # The inner key corresponds to the reception capability of the targeted region and points towards the function which is to be called during the linking event
        # Therefore, it is possible to map e.g. incomimg positional data to the color of the receiving region.
        #
        # Example with SI-integrated linking of positions for reception case:
        # self.cap_link_recv[PySI.POSITION][PySI.POSITION] = self.<function_position_emit>
        # self.cap_link_recv[PySI.POSITION][PySI.COLOR] = self.<function_color_emit>
        # Therefore, this example receives the positional data of a linked region and can apply this data to other categories of data according to the linking relationship.

        # Example with custom capability for linking:
        # self.cap_link_recv[<name of emission capability>][<name of reception capability>] = self.<corresponding function>
        # Therefore, this example receives some data of a linked region and can apply this data to other categories of data according to the linking relationship .
        self.cap_link_recv = PySI.String2String2FunctionMapMap()

        ## member attribute variable storing the x position of the mouse cursor
        self.mouse_x = 0

        ## member attribute variable storing the y position of the mouse cursor
        self.mouse_y = 0

        ## member attribute variable storing whether deletion can be undone/redone
        self.__unredoable_deletion__ = False

    ## member function for retrieving all effects currently represented as regions
    #
    # @return the list of effects as a list
    def current_regions(self) -> list:
        return  self.__current_regions__()

    ## member function for retrieving the maximum width of a region
    #
    # @param self the pointer to the object
    #
    # @return the width of the associated region as int
    def get_region_width(self) -> int:
        if self.aabb[3].x - self.aabb[0].x < 0:
            return 0

        return int(self.aabb[3].x - self.aabb[0].x)

    ## member function for retrieving the maximum height of a region
    #
    # @param self the pointer to the object
    #
    # @return the width of the associated region as int
    def get_region_height(self) -> int:
        if self.aabb[1].y - self.aabb[0].y < 0:
            return 0

        return int(self.aabb[1].y - self.aabb[0].y)

    ## member function for getting the relative x coordinate of the parent region's top left corner
    #
    # @param self the object pointer
    #
    # @return the relative x coordinate of the associated region's top left corner
    def relative_x_pos(self) -> int:
        return self.aabb[0].x

    ## member function for getting the relative y coordinate of the parent region's top left corner
    #
    # @param self the object pointer
    #
    # @return the relative y coordinate of the associated region's top left corner
    def relative_y_pos(self) -> int:
        return self.aabb[0].y

    ## member function for getting the absolute x coordinate of the parent region's top left corner
    #
    # @param self the object pointer
    #
    # @return the absolute x coordinate of the associated region's top left corner
    def absolute_x_pos(self) -> int:
        return self.x + self.aabb[0].x

    ## member function for getting the absolute y coordinate of the parent region's top left corner
    #
    # @param self the object pointer
    #
    # @return the absolute y coordinate of the associated region's top left corner
    def absolute_y_pos(self) -> int:
        return self.y + self.aabb[0].y

    ## member function for enabling the emission or reception of an effect
    #
    # This function is used in order to register collision events.
    # During loading of plugins, the SIGRun plugin transpiler adds this function to the constructor of transpiled plugins based on the information provided in the associated Decorator
    #
    # @param self the object pointer
    # @param capability the capability of the collision event (str)
    # @param is_emit the variable depicting if a region emits (True) or receives (False) an effect (bool)
    # @param on_enter the function to be called for the collision event PySI.ON_ENTER
    # @param on_continuous the function to be called for the collision event PySI.ON_CONTINUOUS
    # @param on_leave the function to be called for the collision event PySI.ON_LEAVE
    #
    # @see on_enter(capability, transmission_type):
    # @see on_continuous(capability, transmission_type):
    # @see on_leave(capability, transmission_type):
    #
    # @return None
    def enable_effect(self, capability: str, is_emit: bool, on_enter: object, on_continuous: object, on_leave: object) -> None:
        if is_emit:
            self.cap_emit[capability] = {PySI.CollisionEvent.ON_ENTER: on_enter, PySI.CollisionEvent.ON_CONTINUOUS: on_continuous, PySI.CollisionEvent.ON_LEAVE: on_leave}
        else:
            self.cap_recv[capability] = {PySI.CollisionEvent.ON_ENTER: on_enter, PySI.CollisionEvent.ON_CONTINUOUS: on_continuous, PySI.CollisionEvent.ON_LEAVE: on_leave}

    ## member function for determining whether a collision event exists
    #
    # @param self the object pointer
    # @param capability the capability of the collision event (str)
    # @param is_emit the transmission type (bool)
    #
    # @return True if a collision event exists with the given capability and transmission type, False else
    def is_effect_enabled(self, capability: str, is_emit: bool) -> bool:
        if is_emit:
            return capability in self.cap_emit

        return capability in self.cap_recv

    ## member function for overriding the emission or reception of an effect
    #
    # @param self the object pointer
    # @param capability the capability of the collision event (str)
    # @param is_emit the variable depicting if a region emits (True) or receives (False) an effect (bool)
    # @param on_enter the function to be called for the collision event PySI.ON_ENTER
    # @param on_continuous the function to be called for the collision event PySI.ON_CONTINUOUS
    # @param on_leave the function to be called for the collision event PySI.ON_LEAVE
    #
    # This function then calls self.enable_effect(capability, is_emit, on_enter, on_continuous, on_leave)
    # @see self.enable_effect(capability, is_emit, on_enter, on_continuous, on_leave)
    #
    # @return None
    def override_effect(self, capability: str, is_emit: bool, on_enter: object, on_continuous: object, on_leave: object) -> None:
        self.enable_effect(capability, is_emit, on_enter, on_continuous, on_leave)

    ## member function for disabling the emission or reception of an effect
    #
    # @param self the object pointer
    # @param capability the capability of the collision event (str)
    # @param is_emit the variable depicting if a region emits (True) or receives (False) an effect (bool)
    #
    # @return None
    def disable_effect(self, capability: str, is_emit: bool) -> None:
        if is_emit:
            if capability in self.cap_emit:
                del self.cap_emit[capability]
        else:
            if capability in self.cap_recv:
                del self.cap_recv[capability]

    ## member function for enabling the emission of data in the context of a link event
    #
    # This function is used in order to register linking actions for emission.
    # During loading of plugins, the SIGRun plugin transpiler adds this function to the constructor of transpiled plugins based on the information provided in the associated decorator.
    #
    # @param self the object pointer
    # @param emission_capability the capability of the linking event (str)
    # @param emission_function the function to be called for emitting data
    #
    # @see on_link(transmission_type, emission_capability, reception_capability=None)
    #
    # @return None
    def enable_link_emission(self, emission_capability: str, emission_function: object) -> None:
        self.cap_link_emit[emission_capability] = emission_function

    ## member function for enabling the emission of data in the context of a link event
    #
    # This function is used in order to register linking actions for reception.
    # During loading of plugins, the SIGRun plugin transpiler adds this function to the constructor of transpiled plugins based on the information provided in the associated decorator.
    #
    # @param self the object pointer
    # @param emission_capability the capability of the linking event used by the emitting region (str)
    # @param reception_capability the capability of the linking event of a receiving region (str)
    # @param reception_function the function to be called for receiving data
    #
    # @see on_link(transmission_type, emission_capability, reception_capability=None)
    #
    # @return None
    def enable_link_reception(self, emission_capability: str, reception_capability: str, reception_function: object) -> None:
        if emission_capability in self.cap_link_recv:
            self.cap_link_recv[emission_capability][reception_capability] = reception_function
        else:
            self.cap_link_recv[emission_capability] = {reception_capability: reception_function}

    ## member function for disabling the emission of data in the context of a link event
    #
    # @param self the object pointer
    # @param emission_capability the capability of the linking event used by the emitting region (str)
    #
    # @return None
    def disable_link_emission(self, emission_capability: str) -> None:
        del self.cap_link_emit[emission_capability]

    ## member function for disabling the reception of data in the context of a link event
    #
    # @param self the object pointer
    # @param emission_capability the capability of the linking event used by the emitting region (str)
    # @param reception_capability the capability of the linking event of a receiving region with default value "" (str)
    #
    # If no reception_capability is specified, the emission_capability is deleted from self.cap_link_recv.
    # If reception_capability is specified and present in self.cap_link_recv, the specified relation is deleted from emission_capability.
    #
    # @see self.cap_link_recv
    #
    # @return None
    def disable_link_reception(self, emission_capability: str, reception_capability: str="") -> None:
        if reception_capability == "":
            if emission_capability in self.cap_link_recv:
                del self.cap_link_recv[emission_capability]
        else:
            if emission_capability in self.cap_link_recv:
                if reception_capability in self.cap_link_recv[emission_capability]:
                    del self.cap_link_recv[emission_capability][reception_capability]

    ## member function for establishing a specified link between two regions according to given attributes
    #
    # @param self the object pointer
    # @param sender_uuid the uuid of the emitting region (str)
    # @param sender_attribute the attribute to be linked by the emitting region (str)
    # @param receiver_uuid the uuid of the receiving region (str)
    # @param receiver_attribute the attribute to be linked by the receiving region (str)
    #
    # @return None
    def create_link(self, sender_uuid: str, sender_attribute: str, receiver_uuid: str, receiver_attribute: str) -> None:
        if sender_uuid != "" and sender_attribute != "" and receiver_uuid != "" and receiver_attribute != "":
            self.link_relations.append([sender_uuid, sender_attribute, receiver_uuid, receiver_attribute])

    ## member function for removing a specified link between two regions according to given attributes
    #
    # @param self the object pointer
    # @param sender_uuid the uuid of the emitting region (str)
    # @param sender_attribute the attribute to be linked by the emitting region (str)
    # @param receiver_uuid the uuid of the receiving region (str)
    # @param receiver_attribute the attribute to be linked by the receiving region (str)
    #
    # @return None
    def remove_link(self, sender_uuid: str, sender_attribute: str, receiver_uuid: str, receiver_attribute: str) -> None:
        if sender_uuid != "" and sender_attribute != "" and receiver_uuid != "" and receiver_attribute != "":
            lr = PySI.LinkRelation(sender_uuid, sender_attribute, receiver_uuid, receiver_attribute)

            if lr in self.link_relations:
                del self.link_relations[self.link_relations.index(lr)]

    ## member function for emitting a linking action
    #
    # @param sender the source of the the linking action
    # @param capability the capability with which the linking action shall be emitted
    # @param args the data which is to be received by receivers
    #
    # @return None
    def emit_linking_action(self, sender: object, capability: str, args: tuple) -> None:
        self.__emit_linking_action__(sender, capability, args)

    ## member function for setting data in the associated qml file of a region effect
    #
    # @param self the object pointer
    # @param key the variable specified in the qml file (str)
    # @param value the value to set in the variable in the qml file (variant)
    # @param datatype the data type of the value (PySI.INT, PySI.FLOAT, ...) (int)
    #
    # @return None
    def set_QML_data(self, key: str, value: object, datatype: int, data_kwargs={}) -> None:
        self.__set_data__(key, value, datatype, data_kwargs)

    ## member function for getting data set from an associated qml file of a region effect
    #
    # @param self the object pointer
    # @param key the key specified in QML to address the required data
    # @param datatype the data type of the requested value (PySI.DataType.INT, PySI.DataType.FLOAT, ...) (int)
    #
    # @return the value queried by the key as the given datatype
    def get_QML_data(self, key: str, datatype: int) -> object:
        return self.__data__(key, datatype)

    ## member function for setting the path to an plugin's associated qml file
    #
    # @param self the object pointer
    # @param filename the file name of the target qml file
    #
    # @return the absolute path to the qml file (str)
    def set_QML_path(self, filename: str) -> str:
        return os.path.dirname(os.path.abspath((inspect.stack()[1])[1])) + "/" + filename

    ## member function for adding a point to a region drawing based on a cursor id.
    #
    # @param self the object pointer
    # @param x the x coordinate of the cursor (float)
    # @param y the y coordinate of the cursor (float)
    # @param cursor_id the id of cursor currently drawing (str)
    #
    # This function is specific to effects of PySI.EffectType.SI_CANVAS.
    # Therefore, this function does nothing when called with other effect types.
    #
    # @return None
    def add_point_to_region_drawing(self, x: float, y: float, cursor_id: str) -> None:
        if self.region_type is int(PySI.EffectType.SI_CANVAS):
            if cursor_id not in self.__partial_regions__.keys():
                self.__partial_regions__[cursor_id] = PySI.PointVector()

            self.__partial_regions__[cursor_id].append([x, y])

    ## member function for registering a region drawing according to a cursor id
    #
    # @param self the object pointer
    # @param cursor_id the id of the cursor which is currently drawing (str)
    #
    # This function is specific to effects of PySI.EffectType.SI_CANVAS.
    # Therefore, this function does nothing when called with other effect types.
    #
    # @return None
    def register_region_from_drawing(self, cursor_id: str) -> None:
        if self.region_type is int(PySI.EffectType.SI_CANVAS):
            self.__registered_regions__.append(cursor_id)

    ## member function for starting the standard application of a file given its uuid as a region and its path in the filesystem
    #
    # @param self the object pointer
    # @param file_uuid the uuid of the region associated to a file icon representing a file of the filesystem (str)
    # @param file_path the path of the file in the filesystem (str)
    #
    # @return None
    def start_standard_application(self, file_uuid: str, file_path: str) -> None:
        self.__embed_file_standard_appliation_into_context__(file_uuid, file_path)

    ## member function for closing the standard application of a file given its uuid as a region and its path in the filesystem
    #
    # @param self the object pointer
    # @param file_uuid the uuid of the region associated to a file icon representing a file of the filesystem (str)
    #
    # @return None
    def close_standard_application(self, file_uuid: str) -> None:
        self.__destroy_embedded_window__(file_uuid)

    ## member function for displaying the contents of a folder in the filesystem as pages of other filesystem entries
    #
    # @param self the object pointer
    # @param page the number of the current page which browsed in a folder region
    # @param source_uuid the uuid of the region associated to a folder icon representing a folder of the filesystem (str)
    # @param with_buttons a flag depicting whether buttons for browsing pages is wanted (True) or not (False) (bool)
    #
    # @return None
    def display_folder_contents_page(self, page: int, source_uuid: str, with_buttons=True) -> None:
        self.__show_folder_contents_page__(page, source_uuid, with_buttons)

    ## member function for deleting a region
    #
    # @param self the object pointer
    #
    # @return None
    def delete(self, uuid:str=None) -> None:
        if uuid is None:
            self.__signal_deletion__()
        else:
            self.__signal_deletion_by_uuid__(uuid)

    ## member function for creating a new region
    #
    # @param self the object pointer
    # @param shape the shape / contour of the region as a PySI.PointVector or list [[x1, x1], [x2, y2], ... [xn, yn]]
    # @param effect_name the name (region_name) of the effect which shall be assigned to the region (region_display_name does not work)
    #
    # @return None
    def create_region_via_name(self, shape: PySI.PointVector, effect_name: str, as_selector=False, kwargs={}) -> None:
        self.__create_region__(shape, effect_name, as_selector, kwargs)

    ## member function for creating a new region
    #
    # @param self the object pointer
    # @param shape the shape / contour of the region as a PySI.PointVector or list [[x1, x1], [x2, y2], ... [xn, yn]]
    # @param effect_name the name (region_name) of the effect which shall be assigned to the region (region_display_name does not work)
    #
    # @return None
    def create_region_via_id(self, shape: PySI.PointVector, effect_type: str, kwargs={}) -> None:
        self.__create_region__(shape, effect_type, kwargs)

    ## member function for retrieving the plugins which are available for sketching as a dict of names.
    # This dict of names uses region_name attributes as keys and region_display_name attributes as values
    #
    # @param self the object pointer
    #
    # @return a list containing all names of available plugins as str values
    def available_plugins(self) -> list:
        return list(self.__available_plugins_by_name__())

    ## member function for snapping a region's center to the mouse cursor
    #
    # @param self the object pointer
    #
    # @return None
    def snap_to_mouse(self) -> None:
        self.x = self.mouse_x - self.relative_x_pos() - self.width / 2
        self.y = self.mouse_y - self.relative_y_pos() - self.height / 2

    ## member function for retrieving the dimensions of the active SI-Context (width in px, and height in px)
    #
    # @param self the object pointer
    #
    # @return the dimensions of the active SI context as a tuple
    def context_dimensions(self) -> tuple:
        return self.__context_dimensions__

    ## member function for assigning a new effect to a region
    # if the region is a cursor, the effect that cursor can draw is changed instead!
    #
    # @param self the object pointer
    # @param effect_name_to_assign the name of the effect which is intended to be written to a region
    # @param effect_display_name the name of the effect which is intended to be visible to a user
    # @param kwargs key-worded arguments containing specifics of certain regions
    #
    # @return None
    def assign_effect(self, effect_name_to_assign: str, effect_display_name: str, kwargs: dict) -> None:
        self.__assign_effect__(self._uuid, effect_name_to_assign, effect_display_name, kwargs)

    ## member function for moving the effect's associated region to the point (x, y)
    #
    # @param self the object pointer
    # @param x the absolute x coordinate of the point
    # @param y the absolute y coordinate of the point
    #
    # @return None
    def move(self, x, y) -> None:
        self.x = x
        self.y = y

    ## member function for generally handling exceptions which may occur in constructors of plugins
    # @author Robert Fent (as part of his Bachelor's Thesis)
    # @param ex the thrown exception as an Exception object
    # @param file the absolute path to the plugin file in which the exception occurred
    #
    # @return None
    def __handle_exception__(self, ex: Exception, file: str) -> None:
        RED_START = '\033[1;31;40m'
        COLOR_END = '\033[0m'
        # remove added dir in filename after transpile
        parsed_file_name = file.replace('__loaded_plugins__/', '')

        # lineno of error in transpiled file
        og_line = ex.__traceback__.tb_lineno

        # vars from user file
        user_line_no = 0
        user_line_content = ''

        # load current file, remove whitespaces and split into lines
        file_lines = open(file).read().replace(' ', '').split('\n')

        # get string of line in current file where error occurred
        error_line = file_lines[og_line-1]

        # load user generated file where we want the line number and remove whitespaces and split lines
        user_file_lines = open(parsed_file_name).read().replace(' ', '').split('\n')

        for line_no, line_content in enumerate(user_file_lines, 1):
            if error_line in line_content:
                user_line_no = line_no
                user_line_content = line_content

        print(
            '\n%s%s occured in file:\n'
            '%s\n'
            'Line number: %s\n'
            'Line content: %s%s'
            % (RED_START, type(ex).__name__, parsed_file_name, str(user_line_no),  user_line_content.replace('\t', ''), COLOR_END))