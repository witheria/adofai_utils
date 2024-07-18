# (c) Witheria 2024

import math

from .MapData import MapData

from .Actions import *
from .AngleConverter import AngleConverter
from .Tile import Tile
from .TileData import TileData
from .Enums import EventType, SpeedType, TileAngle
from .Drawer import CoordinatePlotter
# from .pygame_drawer import CoordinatePlotter


class Map(MapData):
    """
    Represents a full adofai map

    Contains a tile list with all tiles this map contains.
    On initialization analyzes the entirety of the map.

    Either path or map_data needs to be given.

    fields:
        tile_list: list[Tile]: A list of all tiles this map contains.

    functions:
        plot: Plots a map with tkinter

    :param path: A path to the map file.
    :param map_data: A map data object. Either of these parameters needs to be given.
    """
    tile_list: list[Tile]

    def __init__(self, path: str = None, map_data: MapData = None):
        if not map_data and path:
            map_data = MapData()
            map_data.load(path)
        else:
            raise AttributeError('Either map data or path must be provided.')

        super().__init__(map_data.MapSetting, map_data.tile_data_list)
        self.tile_list = list()
        self.bpm = self.MapSetting.bpm
        self.reverse = False
        self.now: TileData = self.tile_data_list[0]
        self.next_tile: TileData | None = None
        self.static_angle = 0

        self.x = 0.0
        self.y = 0.0

        for idx in range(len(map_data.tile_data_list[1:])):
            self.next_tile = map_data.tile_data_list[idx]
            action_list = self.now.get(EventType.SET_SPEED, None)
            if action_list:
                set_speed: SetSpeed = action_list[0]
                if not set_speed.speedType or SpeedType.BPM.name == set_speed.speedType:
                    self.bpm = set_speed.beatsPerMinute
                elif SpeedType.MULTIPLIER.name == set_speed.speedType:
                    self.bpm *= set_speed.bpmMultiplier
                else:
                    print(f"E> Wrong speed type: {set_speed.speedType}")

            if EventType.TWIRL in self.now:
                self.reverse = not self.reverse

            new_angle = AngleConverter.convert_angle(self.static_angle, self.next_tile.tile_angle, reverse=self.reverse,
                                                     now=self.now.tile_angle,
                                                     not_none=self.now.tile_angle != TileAngle.NONE)
            relative_angle = new_angle.relative_angle
            self.tile_list.append(Tile(self.now.floor, self.now.tile_angle, self.now.action_list_map, self.bpm,
                                       relative_angle, self.static_angle, self.reverse, self.x, self.y))

            self.static_angle = new_angle.static_angle

            radians = math.radians(self.static_angle)
            self.x += math.cos(radians)
            self.y += math.sin(radians)

            action_list = self.next_tile.get(EventType.POSITION_TRACK, None)
            if action_list:
                position_track: PositionTrack = action_list[0]
                if position_track.editorOnly == "Disabled":
                    self.x = position_track.positionOffset[0]
                    self.y = position_track.positionOffset[1]

            self.now = self.next_tile

        if self.next_tile:
            if EventType.TWIRL in self.next_tile:
                self.reverse = not self.reverse

            self.tile_list.append(Tile(self.next_tile.floor, self.next_tile.tile_angle, self.next_tile.action_list_map,
                                       self.bpm, 180, self.static_angle, self.reverse, self.x, self.y))

    def plot(self):
        """ """
        # plt = CoordinatePlotter()
        plt = CoordinatePlotter(tile_list=self.tile_list)
        plt.mainloop()
