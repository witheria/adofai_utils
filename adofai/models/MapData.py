# (c) Witheria 2024
import json
import os
from typing import Any

from .Actions import Saveable
from .MapModule import MapModule
from .TileData import TileData
from .Enums import TileAngle

import inspect


def with_kwargs(func):
    """Decorate a function with its own keyword arguments.
    
    Keyword arguments are given with a separate _kwargs parameter.

    :param func: The function to be decorated.
    :returns: The decorated function.

    """
    sig = inspect.signature(func)

    def inner(*args, **kwargs):
        """

        :param args: list of arguments
        :param kwargs: dict of keyword arguments

        """
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()
        _kwargs = bound.arguments
        del _kwargs["_kwargs"]
        return func(*args, **kwargs, _kwargs=_kwargs)

    return inner


def exclude_key_from_dict(_input: dict, key: object) -> dict:
    """returns the same dictionary, but without the key specified

    :param _input: dictionary to exclude the key from
    :param key: the key to be excluded
    :returns: the dictionary without the key

    """
    return {k: value for k, value in _input.items() if k != key}


def group_dicts_by_key(_dict: list[dict], key: str | int | object) -> dict[str | int | object, list[Any]]:
    """Helper function for grouping dictionaries by key.
    
    If a dictionary does not have the key specified, it will not be returned.

    :param _dict: list[dict]: list of dictionaries to group
    :param key: str | int | object: the key to be grouped
    :returns: the grouped dictionaries by key as a list of dictionaries

    """
    result = {}
    for dictionary in _dict:
        if not isinstance(dictionary, dict):
            continue
        _key = dictionary.get(key, None)
        if not _key:
            continue
        if not result.get(_key, None):
            result[_key] = []
        result[_key].append(exclude_key_from_dict(dictionary, key))
    return result


class MapSetting(Saveable):

    """This class interfaces the adofai map settings.
    Internally, this class has a dictionary of default parameters, and any keyword parameters that don't get set by the
    user are filled up with the default values.
    
    The keyword parameter _kwargs is not to be used when creating this class.
    
    This class inherits from Saveable.

    :param version: int
    :param artist: str
    :param specialArtistType: str
    :param artistPermission: str
    :param song: str
    :param author: str
    :param separateCountdownTime: bool
    :param previewImage: str
    :param previewIcon: str
    :param previewIconColor: str hex value
    :param previewSongStart: int
    :param previewSongDuration: int
    :param seizureWarning: bool
    :param levelDesc: str
    :param levelTags: str
    :param artistLinks: str
    :param speedTrialAim: int
    :param difficulty: int
    :param requiredMods: list of mods (given as str)
    :param songFilename: str
    :param bpm: float
    :param volume: int
    :param offset: float
    :param pitch: float
    :param hitsound: str
    :param hitsoundVolume: float
    :param countdownTicks: int
    :param trackColorType: str
    :param trackColor: str hex value
    :param secondaryTrackColor: str hex value
    :param trackColorAnimDuration: float
    :param trackColorPulse: str
    :param trackPulseLength: float
    :param trackStyle: str
    :param trackTexture: str
    :param trackTextureScale: float
    :param trackGlowIntensity: float
    :param trackAnimation: str
    :param beatsAhead: int
    :param trackDisappearAnimation: str
    :param beatsBehind: int
    :param backgroundColor: str hex value
    :param showDefaultBGIfNoImage: bool
    :param showDefaultBGTile: bool
    :param defaultBGTileColor: str hex value
    :param defaultBGShapeType: str
    :param defaultBGShapeColor: str hex value
    :param bgImage: str
    :param bgImageColor: str hex value
    :param parallax: parallax float values (given as list)
    :param bgDisplayMode: str
    :param imageSmoothing: bool
    :param lockRot: bool
    :param loopBG: bool
    :param scalingRatio: int
    :param relativeTo: bool
    :param position: position integer values (given as list)
    :param rotation: float
    :param zoom: float
    :param pulseOnFloor: bool
    :param startCamLowVFX: bool
    :param bgVideo: str
    :param loopVideo: bool
    :param vidOffset: float
    :param floorIconOutlines: bool
    :param stickToFloors: bool
    :param planetEase: str
    :param customClass: str
    :param planetEaseParts: int
    :param planetEasePartBehavior: str
    :param defaultTextColor: str hex value
    :param defaultTextShadowColor: str hex value
    :param congratsText: str
    :param perfectText: str
    :param legacyFlash: bool
    :param legacyCamRelativeTo: bool
    :param legacySpriteTiles: bool

    """

    # Default values for the keyword parameters
    _defaults_dict = {
        'version': 13,
        'artist': '',
        'specialArtistType': 'None',
        'artistPermission': '',
        'song': '',
        'author': '',
        'separateCountdownTime': True,
        'previewImage': '',
        'previewIcon': '',
        'previewIconColor': '003f52',
        'previewSongStart': 0,
        'previewSongDuration': 10,
        'seizureWarning': False,
        'levelDesc': '',
        'levelTags': '',
        'artistLinks': '',
        'speedTrialAim': 0,
        'difficulty': 1,
        'requiredMods': [],
        'songFilename': '',
        'bpm': 100,
        'volume': 100,
        'offset': 0,
        'pitch': 100,
        'hitsound': 'Kick',
        'hitsoundVolume': 100,
        'countdownTicks': 4,
        'trackColorType': 'Single',
        'trackColor': 'debb7b',
        'secondaryTrackColor': 'ffffff',
        'trackColorAnimDuration': 2,
        'trackColorPulse': 'None',
        'trackPulseLength': 10,
        'trackStyle': 'Standard',
        'trackTexture': '',
        'trackTextureScale': 1,
        'trackGlowIntensity': 100,
        'trackAnimation': 'None',
        'beatsAhead': 3,
        'trackDisappearAnimation': 'None',
        'beatsBehind': 4,
        'backgroundColor': '000000',
        'showDefaultBGIfNoImage': True,
        'showDefaultBGTile': True,
        'defaultBGTileColor': '101121',
        'defaultBGShapeType': 'Default',
        'defaultBGShapeColor': 'ffffff',
        'bgImage': '',
        'bgImageColor': 'ffffff',
        'parallax': [100, 100],
        'bgDisplayMode': 'FitToScreen',
        'imageSmoothing': True,
        'lockRot': False,
        'loopBG': False,
        'scalingRatio': 100,
        'relativeTo': 'Player',
        'position': [0, 0],
        'rotation': 0,
        'zoom': 100,
        'pulseOnFloor': True,
        'startCamLowVFX': False,
        'bgVideo': '',
        'loopVideo': False,
        'vidOffset': 0,
        'floorIconOutlines': False,
        'stickToFloors': True,
        'planetEase': 'Linear',
        'planetEaseParts': 1,
        'planetEasePartBehavior': 'Mirror',
        'customClass': '',
        'defaultTextColor': 'ffffff',
        'defaultTextShadowColor': '00000050',
        'congratsText': '',
        'perfectText': '',
        'legacyFlash': False,
        'legacyCamRelativeTo': False,
        'legacySpriteTiles': False
    }

    @with_kwargs
    def __init__(self, version=None, artist=None, specialArtistType=None, artistPermission=None, song=None, author=None,
                 separateCountdownTime=None, previewImage=None, previewIcon=None, previewIconColor=None,
                 previewSongStart=None, previewSongDuration=None, seizureWarning=None, levelDesc=None, levelTags=None,
                 artistLinks=None, speedTrialAim=None, difficulty=None, requiredMods=None, songFilename=None, bpm=None,
                 volume=None, offset=None, pitch=None, hitsound=None, hitsoundVolume=None, countdownTicks=None,
                 trackColorType=None, trackColor=None, secondaryTrackColor=None, trackColorAnimDuration=None,
                 trackColorPulse=None, trackPulseLength=None, trackStyle=None, trackTexture=None,
                 trackTextureScale=None, trackGlowIntensity=None, trackAnimation=None, beatsAhead=None,
                 trackDisappearAnimation=None, beatsBehind=None, backgroundColor=None, showDefaultBGIfNoImage=None,
                 showDefaultBGTile=None, defaultBGTileColor=None, defaultBGShapeType=None, defaultBGShapeColor=None,
                 bgImage=None, bgImageColor=None, parallax=None, bgDisplayMode=None, imageSmoothing=None, lockRot=None,
                 loopBG=None, scalingRatio=None, relativeTo=None, position=None, rotation=None, zoom=None,
                 pulseOnFloor=None, bgVideo=None, loopVideo=None, vidOffset=None, floorIconOutlines=None,
                 stickToFloors=None, planetEase=None, planetEaseParts=None, planetEasePartBehavior=None,
                 defaultTextColor=None, defaultTextShadowColor=None, congratsText=None, perfectText=None,
                 legacyFlash=None, legacyCamRelativeTo=None, legacySpriteTiles=None, startCamLowVFX=None,
                 customClass=None, _kwargs=None):
        self.version = version
        self.artist = artist
        self.specialArtistType = specialArtistType
        self.artistPermission = artistPermission
        self.song = song
        self.author = author
        self.separateCountdownTime = separateCountdownTime
        self.previewImage = previewImage
        self.previewIcon = previewIcon
        self.previewIconColor = previewIconColor
        self.previewSongStart = previewSongStart
        self.previewSongDuration = previewSongDuration
        self.seizureWarning = seizureWarning
        self.levelDesc = levelDesc
        self.levelTags = levelTags
        self.artistLinks = artistLinks
        self.speedTrialAim = speedTrialAim
        self.difficulty = difficulty
        self.requiredMods = requiredMods
        self.songFilename = songFilename
        self.bpm = bpm
        self.volume = volume
        self.offset = offset
        self.pitch = pitch
        self.hitsound = hitsound
        self.hitsoundVolume = hitsoundVolume
        self.countdownTicks = countdownTicks
        self.trackColorType = trackColorType
        self.trackColor = trackColor
        self.secondaryTrackColor = secondaryTrackColor
        self.trackColorAnimDuration = trackColorAnimDuration
        self.trackColorPulse = trackColorPulse
        self.trackPulseLength = trackPulseLength
        self.trackStyle = trackStyle
        self.trackTexture = trackTexture
        self.trackTextureScale = trackTextureScale
        self.trackGlowIntensity = trackGlowIntensity
        self.trackAnimation = trackAnimation
        self.beatsAhead = beatsAhead
        self.trackDisappearAnimation = trackDisappearAnimation
        self.beatsBehind = beatsBehind
        self.backgroundColor = backgroundColor
        self.showDefaultBGIfNoImage = showDefaultBGIfNoImage
        self.showDefaultBGTile = showDefaultBGTile
        self.defaultBGTileColor = defaultBGTileColor
        self.defaultBGShapeType = defaultBGShapeType
        self.defaultBGShapeColor = defaultBGShapeColor
        self.bgImage = bgImage
        self.bgImageColor = bgImageColor
        self.parallax = parallax
        self.bgDisplayMode = bgDisplayMode
        self.imageSmoothing = imageSmoothing
        self.lockRot = lockRot
        self.loopBG = loopBG
        self.scalingRatio = scalingRatio
        self.relativeTo = relativeTo
        self.position = position
        self.rotation = rotation
        self.zoom = zoom
        self.pulseOnFloor = pulseOnFloor
        self.bgVideo = bgVideo
        self.loopVideo = loopVideo
        self.vidOffset = vidOffset
        self.floorIconOutlines = floorIconOutlines
        self.stickToFloors = stickToFloors
        self.planetEase = planetEase
        self.planetEaseParts = planetEaseParts
        self.planetEasePartBehavior = planetEasePartBehavior
        self.defaultTextColor = defaultTextColor
        self.defaultTextShadowColor = defaultTextShadowColor
        self.congratsText = congratsText
        self.perfectText = perfectText
        self.legacyFlash = legacyFlash
        self.legacyCamRelativeTo = legacyCamRelativeTo
        self.legacySpriteTiles = legacySpriteTiles
        self.customClass = customClass
        self.startCamLowVFX = startCamLowVFX

        for key in _kwargs.keys():
            if not _kwargs[key]:
                self._defaults_dict[key] = _kwargs[key]
            setattr(self, key, _kwargs[key])


class MapData(Saveable):
    """MapData serves as a baseclass for the adofai map contents. It contains map settings and a tile list.
    
    This class inherits from Saveable and is used as parent for the main Map class.

    :param map_setting: MapSetting
    :param tile_data_list: list[TileData]

    """

    MapSetting: MapSetting
    tile_data_list: list[TileData]

    path: str

    def __init__(self, map_setting: MapSetting = None, tile_data_list: list = None):
        # Sanitizing args
        if not tile_data_list:
            tile_data_list = []

        if not map_setting:
            map_setting = MapSetting()
        self.MapSetting = map_setting
        self.tile_data_list = tile_data_list

    def load(self, path: str = None) -> None:
        """

        :param path: str:  (Default value = None)

        """
        if path is None:
            path = self.path

        if not os.path.exists(path):
            raise FileNotFoundError

        with open(path, 'r', encoding="utf-8-sig") as f:
            _map = json.load(f)

        path_data: str = _map.get('pathData')

        settings: dict = _map.get('settings')
        self.MapSetting.load(settings)

        floor_actions = _map.get('actions')

        if path_data:
            # If the map contains Letters instead of angles, we go down this road
            # @TODO Write angle data initialization
            chars = [char for char in path_data]
            tile_data = TileData(0, TileAngle.NONE)

            actions_by_floor = group_dicts_by_key(floor_actions, "floor")
            # print(actions_by_floor)
            for action in actions_by_floor.get(0, list()):
                tile_data.add_action(action)
            self.tile_data_list.append(tile_data)

            for idx, c in enumerate(chars[2:]):
                _c = chars[idx - 1]
                tile_angle = MapModule.get_char_tile_angle_map().get(_c)
                t_data = TileData(idx, tile_angle)
                for action in actions_by_floor.get(idx, []):
                    t_data.add_action(action)
                self.tile_data_list.append(t_data)

    def save(self, path: str = None, return_as_str: bool = False) -> None | str:
        """
        For extended documentation read the original documentation for this method.

        Saves all fields of this class to a json file (overwrites the old file if path is not given).
        The path must be valid, otherwise this method will raise a FileNotFoundError.

        :param path: str:  (Default value = None)
        :param return_as_str: bool:  (Default value = False)

        """
        if return_as_str:
            return json.dumps(self.tile_data_list, ensure_ascii=False, indent=4)

        if path is None:
            path = self.path

        with open(path, 'w+', encoding="utf-8-sig") as f:
            json.dump(self.tile_data_list, f, ensure_ascii=False, indent=4)
