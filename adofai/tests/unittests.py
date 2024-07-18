import json
import unittest

from adofai.models import Map


class TestMap(unittest.TestCase):



    def setUp(self):
        with open(r"S:\ai\adofai_main\jglfury\JungleFury.adofai", encoding="utf-8-sig") as f:
            map_data = json.load(f)
        self.map = Map(map_data)