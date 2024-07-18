# (c) Witheria 2024

import json

from .Enums import EventType


class Saveable:
    """
    Baseclass which implements save and load methods for classes based on class fields.
    Serves as a parent class for all Action classes, the MapSetting, Map, and MapData

    functions:
        load
        save
    """

    def load(self, load_obj: str | dict):
        """
        Loads all arguments from a dictionary or json object.
        All keys that are available in the object and exist as attributes in the class
        get set to the corresponding value.
        
        :param load_obj: str or dict
        """
        if isinstance(load_obj, dict):
            obj = load_obj
        else:
            obj = json.loads(load_obj)

        for key, value in obj.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def save(self, dict_only: bool = False):
        """
        Saves all attributes and their values from the class this method
        gets called from as a dictionary or json object.

        :param dict_only: bool: Returns a dictionary if true (Default value = False)
        """
        class_fields = {attr: getattr(self, attr) for attr in dir(self)
                        if not callable(getattr(self, attr)) and not attr.startswith("__") and not attr == "event_type"}
        if dict_only:
            return class_fields

        return json.dumps(class_fields, ensure_ascii=False, indent=4)


class Action(Saveable):
    """Baseclass for Action object.

    Defines standard methods for all Action classes.
    """

    def __init__(self, event_type: EventType):
        self.event_type = event_type

    def __str__(self):
        return str(self.event_type)

    def __repr__(self):
        return self.save(dict_only=True)

    @staticmethod
    def convert_to_camel_case(snake_str):
        """

        :param snake_str: 

        """
        return ''.join(x for x in snake_str.replace("_", " ").title() if not x.isspace())

    def load(self, json_dict: str | dict):
        """

        :param json_dict: str | dict:
        :param json_dict: str | dict: 

        """
        if isinstance(json_dict, str):
            json_dict = json.loads(json_dict)

        class_fields = [attr for attr in dir(self)
                        if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for attr in class_fields:
            if attr == "event_type":
                continue
            try:
                conv = attr.replace("_", "")
                setattr(self, attr, json_dict.get(conv, None))
            except KeyError:
                raise TypeError("This is not the correct event class or the input is malformed!")


class AddDecoration(Action):
    """ """

    def __init__(self, decoration_image=None, position=None, relative_to=None, pivot_offset=None,
                 rotation=None, scale=None, depth=None, tag=None):
        super().__init__(event_type=EventType.ADD_DECORATION)
        self.decorationImage = decoration_image
        self.position = position
        self.relativeTo = relative_to
        self.pivotOffset = pivot_offset
        self.rotation = rotation
        self.scale = scale
        self.depth = depth
        self.tag = tag


class AnimateTrack(Action):
    """ """

    trackAnimation: str
    beatsAhead: float
    trackDisappearAnimation: str
    beatsBehind: float

    def __init__(self, track_animation=None, beats_ahead=None, track_disappear_animation=None, beats_behind=None):
        super().__init__(event_type=EventType.ANIMATE_TRACK)
        self.trackAnimation = track_animation
        self.beatsAhead = beats_ahead
        self.trackDisappearAnimation = track_disappear_animation
        self.beatsBehind = beats_behind


class Bloom(Action):
    """ """

    def __init__(self, enabled=None, threshold=None, intensity=None, color=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.BLOOM)
        self.enabled = enabled
        self.threshold = threshold
        self.intensity = intensity
        self.color = color
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class ChangeTrack(Action):
    """ """

    def __init__(self, track_color_type=None, track_color=None, secondary_track_color=None,
                 track_color_anim_duration=None, track_color_pulse=None, track_pulse_length=None, track_style=None,
                 track_animation=None, beats_ahead=None, track_disappear_animation=None, beats_behind=None):
        super().__init__(event_type=EventType.CHANGE_TRACK)
        self.trackColorType = track_color_type
        self.trackColor = track_color
        self.secondaryTrackColor = secondary_track_color
        self.trackColorAnimDuration = track_color_anim_duration
        self.trackColorPulse = track_color_pulse
        self.trackPulseLength = track_pulse_length
        self.trackStyle = track_style
        self.trackAnimation = track_animation
        self.beatsAhead = beats_ahead
        self.trackDisappearAnimation = track_disappear_animation
        self.beatsBehind = beats_behind


class Checkpoint(Action):
    """ """

    def __init__(self):
        super().__init__(event_type=EventType.CHECK_POINT)


class ColorTrack(Action):
    """ """

    def __init__(self, track_color_type=None, track_color=None, secondary_track_color=None,
                 track_color_anim_duration=None,
                 track_color_pulse=None, track_pulse_length=None, track_style=None):
        super().__init__(event_type=EventType.COLOR_TRACK)
        self.trackColorType = track_color_type
        self.trackColor = track_color
        self.secondaryTrackColor = secondary_track_color
        self.trackColorAnimDuration = track_color_anim_duration
        self.trackColorPulse = track_color_pulse
        self.trackPulseLength = track_pulse_length
        self.trackStyle = track_style


class CustomBackground(Action):
    """ """

    def __init__(self, color=None, bg_image=None, image_color=None, parallax=None, bg_display_mode=None, lock_rot=None,
                 loop_bg=None, unscaled_size=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.CUSTOM_BACKGROUND)
        self.color = color
        self.bgImage = bg_image
        self.imageColor = image_color
        self.parallax = parallax
        self.bgDisplayMode = bg_display_mode
        self.lockRot = lock_rot
        self.loopBg = loop_bg
        self.unscaledSize = unscaled_size
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class Flash(Action):
    """ """

    def __init__(self, duration=None, plane=None, start_color=None, start_opacity=None, end_color=None,
                 end_opacity=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.FLASH)
        self.duration = duration
        self.plane = plane
        self.startColor = start_color
        self.startOpacity = start_opacity
        self.endColor = end_color
        self.endOpacity = end_opacity
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class HallOfMirrors(Action):
    """ """

    def __init__(self, enabled=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.HALL_OF_MIRRORS)
        self.enabled = enabled
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class MoveCamera(Action):
    """ """

    def __init__(self, duration=None, relative_to=None, position=None, rotation=None, zoom=None,
                 angle_offset=None, ease=None, event_tag=None):
        super().__init__(event_type=EventType.MOVE_CAMERA)
        self.duration = duration
        self.relativeTo = relative_to
        self.position = position
        self.rotation = rotation
        self.zoom = zoom
        self.angleOffset = angle_offset
        self.ease = ease
        self.eventTag = event_tag


class MoveDecorations(Action):
    """ """

    def __init__(self, duration=None, tag=None, position_offset=None, rotation_offset=None, scale=None,
                 angle_offset=None, ease=None, event_tag=None):
        super().__init__(event_type=EventType.MOVE_DECORATIONS)
        self.duration = duration
        self.tag = tag
        self.positionOffset = position_offset
        self.rotationOffset = rotation_offset
        self.scale = scale
        self.angleOffset = angle_offset
        self.ease = ease
        self.eventTag = event_tag


class MoveTrack(Action):
    """ """

    def __init__(self, start_tile=None, end_tile=None, duration=None, position_offset=None, rotation=None, scale=None,
                 opacity=None, angle_offset=None, ease=None, event_tag=None):
        super().__init__(event_type=EventType.MOVE_TRACK)
        self.startTile = start_tile
        self.endTile = end_tile
        self.duration = duration
        self.positionOffset = position_offset
        self.rotation = rotation
        self.scale = scale
        self.opacity = opacity
        self.angleOffset = angle_offset
        self.ease = ease
        self.eventTag = event_tag


class PositionTrack(Action):
    """ """

    def __init__(self, position_offset=None, editor_only=None):
        super().__init__(event_type=EventType.POSITION_TRACK)
        self.positionOffset = position_offset
        self.editorOnly = editor_only


class RecolorTrack(Action):
    """ """

    def __init__(self, start_tile=None, end_tile=None, track_color_type=None, track_color=None,
                 secondary_track_color=None, track_color_anim_duration=None, track_color_pulse=None,
                 track_pulse_length=None, track_style=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.RECOLOR_TRACK)
        self.startTile = start_tile
        self.endTile = end_tile
        self.trackColorType = track_color_type
        self.trackColor = track_color
        self.secondaryTrackColor = secondary_track_color
        self.trackColorAnimDuration = track_color_anim_duration
        self.trackColorPulse = track_color_pulse
        self.trackPulseLength = track_pulse_length
        self.trackStyle = track_style
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class RepeatEvents(Action):
    """ """

    def __init__(self, repetitions=None, interval=None, tag=None):
        super().__init__(event_type=EventType.REPEAT_EVENTS)
        self.repetitions = repetitions
        self.interval = interval
        self.tag = tag


class SetConditionalEvents(Action):
    """ """

    def __init__(self, perfect_tag=None, hit_tag=None, barely_tag=None, miss_tag=None, loss_tag=None):
        super().__init__(event_type=EventType.SET_CONDITIONAL_EVENTS)
        self.perfectTag = perfect_tag
        self.hitTag = hit_tag
        self.barelyTag = barely_tag
        self.missTag = miss_tag
        self.lossTag = loss_tag


class SetFilter(Action):
    """ """

    def __init__(self, _filter=None, enabled=None, intensity=None, disable_others=None,
                 angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.SET_FILTER)
        self._filter = _filter
        self.enabled = enabled
        self.intensity = intensity
        self.disableOthers = disable_others
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class SetHitsound(Action):
    """ """

    def __init__(self, hitsound=None, hitsound_volume=None):
        super().__init__(event_type=EventType.SET_HITSOUND)
        self.hitsound = hitsound
        self.hitsoundVolume = hitsound_volume


class SetPlanetRotation(Action):
    """ """

    def __init__(self, ease=None, ease_parts=None):
        super().__init__(event_type=EventType.SET_PLANET_ROTATION)
        self.ease = ease
        self.easeParts = ease_parts


class SetSpeed(Action):
    """ """

    def __init__(self, speed_type=None, beats_per_minute=None, bpm_multiplier=None):
        super().__init__(event_type=EventType.SET_SPEED)
        self.speedType = speed_type
        self.beatsPerMinute = beats_per_minute
        self.bpmMultiplier = bpm_multiplier


class ShakeScreen(Action):
    """ """

    def __init__(self, duration=None, strength=None, intensity=None, fade_out=None, angle_offset=None, event_tag=None):
        super().__init__(event_type=EventType.SHAKE_SCREEN)
        self.duration = duration
        self.strength = strength
        self.intensity = intensity
        self.fadeOut = fade_out
        self.angleOffset = angle_offset
        self.eventTag = event_tag


class Twirl(Action):
    """ """

    def __init__(self):
        super().__init__(event_type=EventType.TWIRL)
