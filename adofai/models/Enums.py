# (c) Witheria 2024

from enum import Enum


class EventType(Enum):
    """Enum class for event types

    Contains all relevant event types that can occur on a tile as a tuple of name and whether it can
    only occur once on a tile.

    :param _type: the name of the event type
    :param single_only: a bool value indicating whether this event type can only occur once on a single tile
    """
    SET_SPEED = ("SetSpeed", True)
    TWIRL = ("Twirl", True)
    CHECK_POINT = ("Checkpoint", True)
    CUSTOM_BACKGROUND = ("CustomBackground", False)
    COLOR_TRACK = ("ColorTrack", True)
    ANIMATE_TRACK = ("AnimateTrack", True)
    ADD_DECORATION = ("AddDecoration", False)
    FLASH = ("Flash", False)
    MOVE_CAMERA = ("MoveCamera", False)
    SET_HITSOUND = ("SetHitsound", True)
    RECOLOR_TRACK = ("RecolorTrack", False)
    MOVE_TRACK = ("MoveTrack", False)
    SET_FILTER = ("SetFilter", False)
    HALL_OF_MIRRORS = ("HallOfMirrors", False)
    SHAKE_SCREEN = ("ShakeScreen", False)
    SET_PLANET_ROTATION = ("SetPlanetRotation", True)
    MOVE_DECORATIONS = ("MoveDecorations", False)
    POSITION_TRACK = ("PositionTrack", True)
    REPEAT_EVENTS = ("RepeatEvents", True)
    BLOOM = ("Bloom", False)
    SET_CONDITIONAL_EVENTS = ("SetConditionalEvents", True)
    CHANGE_TRACK = ("ChangeTrack", False)

    def __init__(self, _type: str, single_only: bool):
        self._type = _type
        self._single_only = single_only

    def __str__(self):
        return self._type

    @property
    def type(self):
        """property to return the name of the item
        :return: the name of the item
        :rtype: str"""
        return self._type

    def name(self):
        """Overload alias of type
        :return: the name of the item
        :rtype: str
        """
        return self._type

    @property
    def single_only(self):
        """property to return whether the event type can only occur once on a single tile
         :return: whether the event type can only occur once on a single tile
         :rtype: bool
         """
        return self._single_only


class TileAngle(Enum):
    """Enum class that contains a list of angle values a tile can have.
     Tile angle values are saved as tuple:
     (Angle name as letter, Angle as float, boolean whether it's a dynamic angle or not)
     """
    _0 = ('R', 0, False)
    _15 = ('p', 15, False)
    _30 = ('J', 30, False)
    _45 = ('E', 45, False)
    _60 = ('T', 60, False)
    _75 = ('o', 75, False)
    _90 = ('U', 90, False)
    _105 = ('q', 105, False)
    _120 = ('G', 120, False)
    _135 = ('Q', 135, False)
    _150 = ('H', 150, False)
    _165 = ('W', 165, False)
    _180 = ('L', 180, False)
    _195 = ('x', 195, False)
    _210 = ('N', 210, False)
    _225 = ('Z', 225, False)
    _240 = ('F', 240, False)
    _255 = ('V', 255, False)
    _270 = ('D', 270, False)
    _285 = ('Y', 285, False)
    _300 = ('B', 300, False)
    _315 = ('C', 315, False)
    _330 = ('M', 330, False)
    _345 = ('A', 345, False)
    _5 = ('5', 108, True)
    _6 = ('6', 252, True)
    _7 = ('7', 900.0 / 7.0, True)
    _8 = ('8', 360 - 900.0 / 7.0, True)
    NONE = ('!', 0, True)

    @property
    def name(self):
        """ """
        return self.value[0]

    @property
    def angle(self):
        """ """
        return self.value[1]

    @property
    def dynamic(self):
        """ """
        return self.value[2]


class CameraRelativeTo(Enum):
    """Enum class that contains values to where the camera event type is relative to.
    Can be:
        Player
        Tile
        Global
        LastPosition

    This class has a name parameter that gets set on creation.
    """

    PLAYER = "Player"
    TILE = "Tile"
    GLOBAL = "Global"
    LAST_POSITION = "LastPosition"

    name: str

    def __init__(self, name: str):
        self._name = name


class SpeedType:
    """Enum-like class containing different types of speed change event types

    This speed type class has a name that gets set on creation.

    BPM: Bpm
    MULTIPLIER: Multiplier
    name: str
    """

    BPM = "Bpm"
    MULTIPLIER = "Multiplier"

    name: str

    def __init__(self, name: str):
        self.name = name
