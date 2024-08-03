import math
import numpy as np

from .classes import Angle, Decoration, Savable
from .Actions import Action


def _angle_from_vecs(vec1: np.array, vec2: np.array):
    # Normalize the vectors
    vec1 = vec1 / np.linalg.norm(vec1)
    vec2 = vec2 / np.linalg.norm(vec2)

    # Calculate the dot product
    dot_product = np.dot(vec1, vec2)

    # Calculate the angle using the arccos of the dot product, clipping to handle numerical errors
    ang_raw = np.arccos(np.clip(dot_product, -1.0, 1.0))

    # Calculate the cross product to determine the direction
    cross_product = vec1[0] * vec2[1] - vec1[1] * vec2[0]

    # Adjust the angle for clockwise direction if needed
    if cross_product < 0:
        ang_raw = (2 * np.pi) - ang_raw

    return np.degrees(ang_raw)


def clockwise_angle(angle1_degrees, angle2_degrees):
    # Normalize the angles to the range [0, 360)
    angle1_degrees = angle1_degrees % 360
    angle2_degrees = angle2_degrees % 360

    # Calculate the clockwise angle difference
    angle_difference = (angle1_degrees - angle2_degrees) % 360

    # If the calculated angle difference is negative, adjust to get the correct clockwise angle
    if angle_difference < 0:
        angle_difference += 360

    return angle_difference


class Tile(Savable):
    """ """
    floor: int  # Index of the tile
    in_angle: Angle  # input angle of the tile
    out_angle: Angle  # output angle of the tile
    in_vec: np.array
    out_vec: np.array
    decorations: list[Decoration]  # List of decoration objects on this Tile
    actions: list | dict | list[Action]  # Actions associated with this class
    bpm: float  # The current beats per minute of this tile

    is_short_return_tile: bool
    is_long_return_tile: bool

    relative_angle: float  # The relative angle of this tile
    relative_angle_reverse: float  # The relative angle of this tile if reversed
    reversed: bool  # Whether the rotation on this tile is reversed

    distance_from_start_beats: float  # The distance from the start of the map in beats
    distance_from_start: float  # The distance from the start of the map in milliseconds

    offset_x: float  # The x offset of this Tile, the sum of all x offsets of other tiles before this tile
    offset_y: float  # The y offset of this Tile, the sum of all y offsets of other tiles before this tile
    dur_x: float  # The amount of units this Tile takes up on the x-axis
    dur_y: float  # The amount of units this Tile takes up on the y-axis

    duration: float  # The duration in ms of this Tile
    duration_in_beats: float  # The duration in beats of this Tile

    def __init__(self, floor: int, in_angle: Angle, out_angle: Angle, actions: dict[str, Action] = None,
                 bpm: float = 0.0, _reversed: bool = False, offset_x: float = 0.0,
                 offset_y: float = 0.0, distance_from_start_beats: float = 0.0, distance_from_start: float = 0.0,
                 decorations: list[Decoration] = None, previous_tile: "Tile" = None, is_short_return_tile: bool = False,
                 is_long_return_tile: bool = False):
        self.floor = floor
        self.in_angle = in_angle
        self.out_angle = out_angle
        self.in_vec = np.array(self.angle_to_vector(self.in_angle.angle))
        self.out_vec = np.array(self.angle_to_vector(self.out_angle.angle))

        self.is_short_return_tile = is_short_return_tile
        self.is_long_return_tile = is_long_return_tile

        self.actions = actions if actions else []
        self.decorations = decorations if decorations else []
        self.reversed = _reversed
        self.bpm = bpm

        self.offset_x = offset_x
        self.offset_y = offset_y

        self.distance_from_start = distance_from_start
        self.distance_from_start_beats = distance_from_start_beats

        self.duration_in_beats = 0.0
        self.duration = 0.0
        self.prev_tile = previous_tile
        self.relative_angle = 360.0
        self.relative_angle_reverse = 0.0

        if not is_long_return_tile:
            self.calculate_relative_angle()
        if not is_short_return_tile:
            self.calculate_duration()
        self.calculate_pos_offsets()

    def __repr__(self):
        return self.save()

    def __str__(self):
        return f"""Tile on Floor: {self.floor}, Angle: {self.relative_angle}, BPM: {self.bpm}"""

    def calculate_duration(self) -> None:
        """
        Calculates the duration of an angle in milliseconds and beats.
        If bpm is not given, the duration in milliseconds will be zero.

        After calling this method, self.duration_in_beats and self.duration can be accessed safely
        """
        self.duration_in_beats: float = self.relative_angle / np.float64(180.0)
        self.duration: float = 0.0
        if self.bpm:
            self.duration = self.duration_in_beats * (60_000 / self.bpm)

    @staticmethod
    def angle_to_vector(angle_degrees):
        angle_radians = np.radians(angle_degrees)
        return np.array([np.cos(angle_radians), np.sin(angle_radians)])

    def calculate_relative_angle(self) -> None:
        """
        This function converts the in- and output angles of this tile into a relative angle.
        After calling this method, self.relative_angle and self.relative_angle_reverse can be accessed safely.

        dot = np.dot(self.in_vec, self.out_vec)
        det = np.linalg.det([self.in_vec, self.out_vec])
        self.relative_angle = np.degrees(np.atan2(dot, det))
        """
        if not self.reversed:
            self.relative_angle = clockwise_angle(self.in_angle.angle, self.out_angle.angle)
            self.relative_angle_reverse = 360 - self.relative_angle % 360
        else:
            self.relative_angle_reverse = clockwise_angle(self.in_angle.angle, self.out_angle.angle)
            self.relative_angle = 360 - self.relative_angle_reverse % 360

    def calculate_pos_offsets(self):
        self.dur_x = np.cos(self.out_angle.radians)
        self.dur_y = np.sin(self.out_angle.radians)
