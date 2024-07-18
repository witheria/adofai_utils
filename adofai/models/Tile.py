# (c) Witheria 2024

from .TileData import TileData, TileAngle, EventType, Action


class Tile(TileData):
    """ """
    bpm: float
    relative_angle: float
    static_angle: float
    reversed: bool

    x: float
    y: float

    def __init__(self, floor: int, tile_angle: TileAngle, action_list_map: dict[EventType, list[Action]], bpm: float,
                 relative_angle: float, static_angle: float, _reversed: bool, x: float, y: float):
        super().__init__(floor, tile_angle, action_list=action_list_map)

        self.relative_angle = relative_angle
        self.static_angle = static_angle
        self.reversed = _reversed
        self.bpm = bpm
        self.x = x
        self.y = y

    def set_relative_angle(self, relative_angle: float):
        """
        Sets a relative anglet to the tile. Could be done with a property but sometimes im lazy.

        :param relative_angle: float: 

        """
        if relative_angle < 0 or relative_angle > 360.0:
            raise ValueError('Relative angle must be between 0 and 360')
        self.relative_angle = relative_angle

    def get_bpm(self):
        """ """
        return 180 * self.bpm / self.relative_angle

    def get_reversed_relative_angle(self):
        """Reverses the relative angle of the tile. """
        return self.relative_angle - 360.0 if self.relative_angle == 360.0 else self.relative_angle

    def get_tile_duration(self):
        """Returns the tile duration in milliseconds """
        return 60000.0 / (180.0 * self.bpm) * self.relative_angle

    def get_tile_duration_in_beats(self, get_as_string: bool = False) -> str | float:
        """Returns the tile duration in beats"""
        if get_as_string:
            return self.relative_angle / 180.0
        return self.relative_angle / 180.0
