import json
import os
import re

from adofai import Actions
from .Tile import Tile
from .classes import MapSetting, Angle, Decoration, group_dicts_by_key, Savable
from .Drawer import main, PYGAME_FLAG
from .midi.adofai_to_midi import tiles_to_midi_pretty


def action_name_to_class(action_name: str):
    """
    Converts an action name to the corresponding Actions class.
    """
    # print(f"Looking up action {action_name}")
    try:
        return getattr(Actions, action_name)()
    except AttributeError as e:
        raise AttributeError(f"The name {action_name} is not an event class!\nReraised Exception: {e}")


def remove_trailing_commas(json_string):
    # Regular expression to find trailing commas
    json_string = re.sub(r',\s*([]}])', r'\1', json_string)
    return json_string


class Map(Savable):
    """
    Represents a full adofai map

    Contains a tile list with all tiles this map contains.
    On initialization analyzes the entirety of the map.

    Either path or map_data needs to be given.

    fields:
        tile_list: list[Tile]: A list of all tiles this map contains.

    functions:
        plot: Plots a map with tkinter

    :param path: The path to the map file.
    """
    tile_list: list[Tile]
    base_bpm: float

    # Map parts
    actions: list | dict[str | int, str]
    angle_data: list[Angle]
    settings: MapSetting
    decorations: list[Decoration] | list[dict] | dict

    path: str
    pos_x: float
    pos_y: float

    duration: float
    duration_in_beats: float

    def __init__(self, path: str):

        self.tile_list = []

        self.base_bpm = 0.0

        self.actions = []
        self.angle_data = []
        self.settings = MapSetting()
        self.decorations = []
        self.path = os.path.abspath(path)

        self.pos_x = 0.0
        self.pos_y = 0.0

        self.duration = 0.0
        self.duration_in_beats = 0.0
        self.load()

    def load(self, path: str = None):
        path = path or self.path
        if not path:
            raise AttributeError("No path given!")

        with open(path, 'r', encoding="utf-8-sig") as f:
            data = json.loads(remove_trailing_commas(f.read()))

        try:
            if "angleData" in data:
                self.angle_data = [Angle(descriptor=float(a)) for a in data["angleData"]]
            elif "pathData" in data:
                self.angle_data = [Angle(descriptor=a) for a in data["pathData"]]
            self.settings.load(data["settings"])
            self.base_bpm = float(self.settings.bpm)
            self.decorations = data.get("decorations", [])
            self.actions = data.get("actions", [])

        except KeyError:
            raise AttributeError("This file contains no map data!")

        self.load_tiles()

    def load_tiles(self):
        if not self.angle_data:
            return
        floor = 0
        pos_x = 0.0
        pos_y = 0.0

        self.actions = group_dicts_by_key(self.actions, "floor")
        self.decorations = group_dicts_by_key(self.decorations, "floor")

        def convert_tile_action_dict_to_classes(tile_action_dict):
            return {
                action.get("eventType"):
                    (action_instance := action_name_to_class(action.get("eventType"))).load(action) or action_instance

                for action in tile_action_dict
            }

        # first tile
        tile_actions: dict[str, Actions.Action] = convert_tile_action_dict_to_classes(self.actions.get(floor, []))
        tile_decorations = [Decoration(d) for d in self.decorations.get(floor, [])]
        self.tile_list.append(Tile(
            floor=0, in_angle=Angle(0.0).opposite, out_angle=self.angle_data[0], bpm=self.base_bpm,
            decorations=tile_decorations, actions=tile_actions
        ))
        cur_bpm = self.base_bpm
        is_reversed = False
        pos_x += self.tile_list[-1].dur_x
        pos_y += self.tile_list[-1].dur_y
        distance_from_start = 0.0
        dis_from_start_beats = 0.0

        for floor in range(1, len(self.angle_data)):

            tile_actions: dict[str, Actions.Action] = convert_tile_action_dict_to_classes(self.actions.get(floor, []))
            tile_decorations = [Decoration(d) for d in self.decorations.get(floor, [])]

            is_reversed = not is_reversed if "Twirl" in tile_actions else is_reversed

            # Speed changes
            speed_change: Actions.SetSpeed = tile_actions.get("SetSpeed", None)
            if speed_change:
                if speed_change.speedType == "Bpm":
                    cur_bpm = speed_change.beatsPerMinute
                elif speed_change.speedType == "Multiplier":
                    cur_bpm *= speed_change.bpmMultiplier
                else:
                    raise AttributeError(f"Unknown speed type: {speed_change.speedType}!")

            if self.angle_data[floor] == 999.0:
                # short return tiles (the ones with the triangle)
                tile = Tile(floor=floor, in_angle=self.tile_list[floor - 1].out_angle.opposite,
                            out_angle=self.tile_list[floor - 1].out_angle.opposite, bpm=cur_bpm,
                            is_short_return_tile=True,
                            actions=tile_actions, decorations=tile_decorations, previous_tile=self.tile_list[floor - 1],
                            offset_x=pos_x, offset_y=pos_y, _reversed=is_reversed,
                            distance_from_start=distance_from_start, distance_from_start_beats=dis_from_start_beats)

            elif self.angle_data[floor].angle < 0:
                # long return tiles (the ones with the half circle)
                tile = Tile(floor=floor, in_angle=self.tile_list[floor - 1].out_angle.opposite,
                            out_angle=self.angle_data[floor].opposite, bpm=cur_bpm,
                            is_long_return_tile=True,
                            actions=tile_actions, decorations=tile_decorations, previous_tile=self.tile_list[floor - 1],
                            offset_x=pos_x, offset_y=pos_y, _reversed=is_reversed,
                            distance_from_start=distance_from_start, distance_from_start_beats=dis_from_start_beats)

            else:
                tile = Tile(floor=floor, in_angle=self.tile_list[floor - 1].out_angle.opposite,
                            out_angle=self.angle_data[floor],
                            actions=tile_actions, bpm=cur_bpm, decorations=tile_decorations, _reversed=is_reversed,
                            offset_x=pos_x, offset_y=pos_y, previous_tile=self.tile_list[floor - 1],
                            distance_from_start=distance_from_start, distance_from_start_beats=dis_from_start_beats)
            pos_x += tile.dur_x
            pos_y += tile.dur_y
            distance_from_start += tile.duration
            dis_from_start_beats += tile.duration_in_beats
            self.tile_list.append(tile)
        """
        last_tile = Tile(floor=len(self.angle_data) + 1, in_angle=self.angle_data[-1].opposite,
                         out_angle=Angle(0.0), bpm=cur_bpm)
        self.tile_list.append(last_tile)
        """
        self.duration = self.tile_list[-1].duration
        self.duration_in_beats = self.tile_list[-1].duration_in_beats
        self.pos_x = pos_x
        self.pos_y = pos_y



    """def load_tiles_old(self):
        if not self.angle_data:
            return

        self.tile_list.append(Tile(
            floor=0, tile_angle=Angle(0.0), bpm=self.settings.bpm
        ))
        cur_bpm = self.base_bpm
        is_reversed = False

        self.actions = group_dicts_by_key(self.actions, "floor")
        self.decorations = group_dicts_by_key(self.decorations, "floor")

        for floor, angle in enumerate(self.angle_data[1:]):
            # Actions and decorations
            tile_actions: list[Actions.Action] = [
                (action_instance := action_name_to_class(action.get("eventType"))).load(action) or action_instance
                for action in self.actions.get(floor, [])
            ]
            tile_decorations = [Decoration(d) for d in self.decorations.get(floor, [])]
            is_reversed = not is_reversed \
                if any([t for t in self.tile_list[-1].actions if t.event_type == "Twirl"]) else is_reversed

            # Speed changes
            try:
                speed_change: Actions.SetSpeed = [t for t in tile_actions if t.event_type == "SetSpeed"][0]
                if speed_change.speedType == "Bpm":
                    cur_bpm = speed_change.beatsPerMinute
                elif speed_change.speedType == "Multiplier":
                    cur_bpm *= speed_change.bpmMultiplier
                else:
                    raise AttributeError(f"Unknown speed type: {speed_change.speedType}!")
            except IndexError:
                pass

            self.tile_list[-1].calculate_relative_angle(angle, reverse=is_reversed)

            # Positions
            tile_pos_x = self.pos_x + self.tile_list[-1].dur_x
            tile_pos_y = self.pos_y + self.tile_list[-1].dur_y
            self.pos_x = tile_pos_x
            self.pos_y = tile_pos_y

            # Duration
            start_dur = self.duration
            start_dur_beats = self.duration_in_beats
            tile_dur = self.tile_list[-1].calculate_duration()
            self.duration += tile_dur[0]
            self.duration_in_beats += tile_dur[1]

            self.tile_list.append(Tile(
                floor=floor, tile_angle=angle, actions=tile_actions, bpm=cur_bpm, offset_x=tile_pos_x,
                offset_y=tile_pos_y, _reversed=is_reversed, distance_from_start=start_dur,
                distance_from_start_beats=start_dur_beats, decorations=tile_decorations
            ))"""

    def to_midi(self, path: str = None):
        """
        Converts this map to a midi file

        :param path: Path to save the midi file to. If not given, the file will be created at the map location
        """
        if not path:
            path = os.path.join(
                os.sep.join(self.path.split(os.sep)[:-1]), f"{self.settings.song.replace("\"", "")}.mid")
        if not os.path.exists(os.sep.join(self.path.split(os.sep)[:-1])):
            raise FileNotFoundError("The map directory does not exist!")
        file = open(path, 'wb+')
        file.close()
        tiles_to_midi_pretty(self.tile_list[1:], path)

    def plot(self):
        if not PYGAME_FLAG:
            print("You need to install pygame to use this function!")
            return
        main(self.tile_list)
        return
