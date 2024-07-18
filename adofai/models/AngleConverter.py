# (c) Witheria 2024

from .Enums import TileAngle


class AngleResult:
    """
    This class is used as a return type for the Angle converter.
    It has the following attributes, which should not get changed after initialization.

    fields:
        static_angle: float

        relative_angle: float

     :param static_angle: float
     :param relative_angle: float
     """

    static_angle: float
    relative_angle: float

    def __init__(self, static_angle, relative_angle):
        self.static_angle = static_angle
        self.relative_angle = relative_angle


class AngleConverter(object):
    """Base class for Angle conversion

    Consists of functions to convert static angles into relative angles and letters into angles.

    functions:
        convert_angle
        get_next_letter_angle
        get_next_static_angle

    """

    @staticmethod
    def convert_angle(now_static_angle: float, _next: TileAngle,
                      reverse: bool, not_none: bool, now: TileAngle = None) -> AngleResult:
        """
        This function converts the static angle of two tiles to the relative angle between these tiles.
        Returns an AngleResult object containing both static angle and relative angle between the two tiles.

        :param now_static_angle: float: A static angle of a tile
        :param now: TileAngle: A TileAngle object that can be given instead of the now_static_angle
        :param _next: TileAngle: The static angle of the next tile
        :param reverse: bool: If the rotation direction is reversed
        :param not_none: bool: idk what this does you tell me

        """
        if now:
            now_static_angle = now.angle

        if _next.dynamic:
            static_angle = now_static_angle + _next.angle
            relative_angle = _next.angle

            if static_angle > 360:
                static_angle = static_angle - 360

        else:
            static_angle = _next.angle

            if reverse:
                relative_angle = -now_static_angle + _next.angle
            else:
                relative_angle = -_next.angle + now_static_angle

            if not_none:
                relative_angle = relative_angle + 180

            if relative_angle <= 0:
                relative_angle = relative_angle + 360

            elif relative_angle > 360:
                relative_angle = relative_angle - 360

        return AngleResult(static_angle, relative_angle)

    @staticmethod
    def get_next_letter_angle(static_angle: float, relative_angle: float, reverse: bool):
        """
        Gets the next angle between two tiles. This function is deprecated for old maps.

        :param static_angle: float: The current static angle
        :param relative_angle: float: A current relative angle between two tiles
        :param reverse: bool: If the rotation direction is reversed

        """
        if reverse and relative_angle != 0.0:
            relative_angle = 360 - relative_angle
            if relative_angle <= 0:
                relative_angle += 360
            elif relative_angle > 360:
                relative_angle -= 360

        if relative_angle == 0.0:
            return TileAngle.NONE
        elif relative_angle == 108.0:
            return TileAngle._5
        elif relative_angle == 252.0:
            return TileAngle._6
        elif relative_angle == 900.0 / 7.0:
            return TileAngle._7
        elif relative_angle == 360 - 900.0 / 7.0:
            return TileAngle._8
        elif static_angle == 0.0:
            return TileAngle._0
        elif static_angle == 15.0:
            return TileAngle._15
        elif static_angle == 30.0:
            return TileAngle._30
        elif static_angle == 45.0:
            return TileAngle._45
        elif static_angle == 60.0:
            return TileAngle._60
        elif static_angle == 75.0:
            return TileAngle._75
        elif static_angle == 90.0:
            return TileAngle._90
        elif static_angle == 105.0:
            return TileAngle._105
        elif static_angle == 120.0:
            return TileAngle._120
        elif static_angle == 135.0:
            return TileAngle._135
        elif static_angle == 150.0:
            return TileAngle._150
        elif static_angle == 165.0:
            return TileAngle._165
        elif static_angle == 180.0:
            return TileAngle._180
        elif static_angle == 195.0:
            return TileAngle._195
        elif static_angle == 210.0:
            return TileAngle._210
        elif static_angle == 225.0:
            return TileAngle._225
        elif static_angle == 240.0:
            return TileAngle._240
        elif static_angle == 255.0:
            return TileAngle._255
        elif static_angle == 270.0:
            return TileAngle._270
        elif static_angle == 285.0:
            return TileAngle._285
        elif static_angle == 300.0:
            return TileAngle._300
        elif static_angle == 315.0:
            return TileAngle._315
        elif static_angle == 330.0:
            return TileAngle._330
        elif static_angle == 345.0:
            return TileAngle._345
        else:
            print(f"E> wrong angle : {static_angle}, {relative_angle}")
            return None

    @staticmethod
    def get_next_static_angle(static_angle: float, relative_angle: float, reverse: bool):
        """
        Calculate the next static angle based on an initial angle, a relative angle adjustment,
        and a direction flag, ensuring the result is within the range [0, 360] degrees.

        :param static_angle: float: The initial static angle in degrees.
        :param relative_angle: float: The relative angle by which to adjust the initial angle.
        :param reverse: bool: If True, the relative angle is added and then 180 degrees are subtracted.
                              If False, the relative angle is subtracted and then 180 degrees are added.

        :return: float: The resulting static angle normalized within the range [0, 360] degrees.

        Examples:
        --------
        >>> get_next_static_angle(30.0, 60.0, True)
        270.0

        >>> get_next_static_angle(30.0, 60.0, False)
        150.0

        >>> get_next_static_angle(350.0, 20.0, True)
        190.0

        >>> get_next_static_angle(350.0, 20.0, False)
        150.0
        """
        if reverse:
            static_angle = static_angle + relative_angle - 180
        else:
            static_angle = static_angle - relative_angle + 180

        if static_angle >= 360:
            static_angle = static_angle - 360
        elif static_angle < 0:
            static_angle = static_angle + 360

        return static_angle
