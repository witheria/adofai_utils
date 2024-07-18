# (c) Witheria 2024

from .MapModule import MapModule
from .Enums import TileAngle
from .Actions import *


class TileData:
    """
    Base class for tiles.
    This class is iterable and will use the action_list_map for that.

    attributes:
        floor: int
        tile_angle: TileAngle
        action_list_map: dict[EventType, list[Action]]

    functions:
        add_action: adds an action to this tile
        add_next_tile_action_list_map: adds an already created action list to this tile.


    """
    floor: int
    tile_angle: TileAngle

    action_list_map: dict[EventType, list[Action]]

    def __init__(self, floor, tile_angle, action_list: dict[EventType, list[Action]] = None):
        if action_list is None:
            action_list = dict()

        self.floor = floor
        self.tile_angle = tile_angle
        self.action_list_map = action_list

    def __str__(self):
        return "f:" + str(self.floor) + ", ta:" + self.tile_angle.angle + ", a(" + str(self.action_list_map) + ")"

    def __getitem__(self, key):
        return self.action_list_map.get(key, None)

    def __setitem__(self, key, value):
        self.action_list_map[key] = value

    def __iter__(self):
        return iter(self.action_list_map)

    def __contains__(self, item):
        return item in self.action_list_map

    def get(self, key, default=None):
        """

        :param key: 
        :param default:  (Default value = None)

        """
        return self.action_list_map.get(key, default)

    def add_action(self, action_dict: dict):
        """

        :param action_dict: dict: 

        """
        event_type_string = action_dict.get('eventType')
        string_map = MapModule.get_string_event_type_map()
        event_type = string_map.get(event_type_string)
        if event_type is None:
            print("Event type not found: ", event_type_string, event_type)
            return

        match event_type:
            case EventType.SET_SPEED:
                action = SetSpeed()

            case EventType.TWIRL:
                action = Twirl()

            case EventType.CHECK_POINT:
                action = Checkpoint()

            case EventType.CUSTOM_BACKGROUND:
                action = CustomBackground()

            case EventType.COLOR_TRACK:
                action = ColorTrack()

            case EventType.ANIMATE_TRACK:
                action = AnimateTrack()

            case EventType.ADD_DECORATION:
                action = AddDecoration()

            case EventType.FLASH:
                action = Flash()

            case EventType.MOVE_CAMERA:
                action = MoveCamera()

            case EventType.SET_HITSOUND:
                action = SetHitsound()

            case EventType.RECOLOR_TRACK:
                action = RecolorTrack()

            case EventType.MOVE_TRACK:
                action = MoveTrack()

            case EventType.SET_FILTER:
                action = SetFilter()

            case EventType.HALL_OF_MIRRORS:
                action = HallOfMirrors()

            case EventType.SHAKE_SCREEN:
                action = ShakeScreen()

            case EventType.SET_PLANET_ROTATION:
                action = SetPlanetRotation()

            case EventType.MOVE_DECORATIONS:
                action = MoveDecorations()

            case EventType.POSITION_TRACK:
                action = PositionTrack()

            case EventType.REPEAT_EVENTS:
                action = RepeatEvents()

            case EventType.BLOOM:
                action = Bloom()

            case EventType.SET_CONDITIONAL_EVENTS:
                action = SetConditionalEvents()

            case EventType.CHANGE_TRACK:
                action = ChangeTrack()

            case _:
                action = None

        action.load(action_dict)
        action_list = self.action_list_map.get(event_type)

        if action_list is None:
            action_list = list()
        action_list.append(action)

        self.action_list_map[event_type] = action_list

    def add_next_tile_action_list_map(self, action_list_map: dict[EventType, list[Action]]):
        """

        :param action_list_map: dict[EventType: 

        """
        for event_type, action_list in action_list_map.items():
            if event_type not in self.action_list_map:
                self.action_list_map[event_type] = action_list
            else:
                self.action_list_map[event_type].extend(action_list)
