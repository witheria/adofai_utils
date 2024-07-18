# (c) Witheria 2024

from .Enums import TileAngle, EventType


class MapModule:
    """ """
    string_event_type_map = None
    event_type_string_map = None
    char_tile_angle_map = None
    tile_angle_char_map = None

    @staticmethod
    def get_string_event_type_map():
        """ """
        if MapModule.string_event_type_map is None:
            MapModule.string_event_type_map = {
                EventType.SET_SPEED.value[0]: EventType.SET_SPEED,
                EventType.TWIRL.value[0]: EventType.TWIRL,
                EventType.CHECK_POINT.value[0]: EventType.CHECK_POINT,
                EventType.CUSTOM_BACKGROUND.value[0]: EventType.CUSTOM_BACKGROUND,
                EventType.COLOR_TRACK.value[0]: EventType.COLOR_TRACK,
                EventType.ANIMATE_TRACK.value[0]: EventType.ANIMATE_TRACK,
                EventType.ADD_DECORATION.value[0]: EventType.ADD_DECORATION,
                EventType.FLASH.value[0]: EventType.FLASH,
                EventType.MOVE_CAMERA.value[0]: EventType.MOVE_CAMERA,
                EventType.SET_HITSOUND.value[0]: EventType.SET_HITSOUND,
                EventType.RECOLOR_TRACK.value[0]: EventType.RECOLOR_TRACK,
                EventType.MOVE_TRACK.value[0]: EventType.MOVE_TRACK,
                EventType.SET_FILTER.value[0]: EventType.SET_FILTER,
                EventType.HALL_OF_MIRRORS.value[0]: EventType.HALL_OF_MIRRORS,
                EventType.SHAKE_SCREEN.value[0]: EventType.SHAKE_SCREEN,
                EventType.SET_PLANET_ROTATION.value[0]: EventType.SET_PLANET_ROTATION,
                EventType.MOVE_DECORATIONS.value[0]: EventType.MOVE_DECORATIONS,
                EventType.POSITION_TRACK.value[0]: EventType.POSITION_TRACK,
                EventType.REPEAT_EVENTS.value[0]: EventType.REPEAT_EVENTS,
                EventType.BLOOM.value[0]: EventType.BLOOM,
                EventType.SET_CONDITIONAL_EVENTS.value[0]: EventType.SET_CONDITIONAL_EVENTS,
                EventType.CHANGE_TRACK.value[0]: EventType.CHANGE_TRACK,
            }
        return MapModule.string_event_type_map

    @staticmethod
    def get_event_type_string_map():
        """ """
        if MapModule.event_type_string_map is None:
            MapModule.event_type_string_map = {v: k for k, v in MapModule.get_string_event_type_map().items()}
        return MapModule.event_type_string_map

    @staticmethod
    def get_char_tile_angle_map():
        """ """
        if MapModule.char_tile_angle_map is None:
            MapModule.char_tile_angle_map = {
                TileAngle._0.name: TileAngle._0,
                TileAngle._15.name: TileAngle._15,
                TileAngle._30.name: TileAngle._30,
                TileAngle._45.name: TileAngle._45,
                TileAngle._60.name: TileAngle._60,
                TileAngle._75.name: TileAngle._75,
                TileAngle._90.name: TileAngle._90,
                TileAngle._105.name: TileAngle._105,
                TileAngle._120.name: TileAngle._120,
                TileAngle._135.name: TileAngle._135,
                TileAngle._150.name: TileAngle._150,
                TileAngle._165.name: TileAngle._165,
                TileAngle._180.name: TileAngle._180,
                TileAngle._195.name: TileAngle._195,
                TileAngle._210.name: TileAngle._210,
                TileAngle._225.name: TileAngle._225,
                TileAngle._240.name: TileAngle._240,
                TileAngle._255.name: TileAngle._255,
                TileAngle._270.name: TileAngle._270,
                TileAngle._285.name: TileAngle._285,
                TileAngle._300.name: TileAngle._300,
                TileAngle._315.name: TileAngle._315,
                TileAngle._330.name: TileAngle._330,
                TileAngle._345.name: TileAngle._345,
                TileAngle._5.name: TileAngle._5,
                TileAngle._6.name: TileAngle._6,
                TileAngle._7.name: TileAngle._7,
                TileAngle._8.name: TileAngle._8,
                TileAngle.NONE.name: TileAngle.NONE,
            }
        return MapModule.char_tile_angle_map

    @staticmethod
    def get_tile_angle_char_map():
        """ """
        if MapModule.tile_angle_char_map is None:
            MapModule.tile_angle_char_map = {v: k for k, v in MapModule.get_char_tile_angle_map().items()}
        return MapModule.tile_angle_char_map
