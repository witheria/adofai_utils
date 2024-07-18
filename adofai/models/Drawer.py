# (c) Witheria 2024

import time
import tkinter as tk
from math import sqrt

from adofai.models import Tile


class CoordinatePlotter(tk.Tk):
    tile_list: list[Tile]
    scale: float
    coordinate_scale: float

    def __init__(self, coordinates: list[tuple] = None, tile_list: list[Tile] = None):
        super().__init__()

        self.title("Coordinate Plotter")
        self.geometry("800x800")

        if coordinates is None:
            coordinates = []

        if tile_list:
            self.tile_list = tile_list

        self.last_redraw_time = 0
        self.redraw_delay = 50  # milliseconds

        self._objects = []

        self.canvas = tk.Canvas(self, bg="white", width=800, height=800)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.coordinates = coordinates
        self.scale = 20.0
        self.coordinate_scale = self.scale / 10
        self.offset_x = 0
        self.offset_y = 0
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.info_label = tk.Label(self, text="", bg="lightyellow", bd=1, relief=tk.SOLID)

        self.plot_points()
        self.draw_lines() if not self.tile_list else self.draw_lines(draw_from_tiles=True)

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.on_zoom)

    def _calc_canvas_coordinates(self, x1, y1, x2, y2):
        canvas_x1 = self.transform_x(x1)
        canvas_y1 = self.transform_y(y1)
        canvas_x2 = self.transform_x(x2)
        canvas_y2 = self.transform_y(y2)
        return canvas_x1, canvas_y1, canvas_x2, canvas_y2

    def _redraw_canvas(self):
        print("redrawing canvas")
        current_time = int(time.time() * 1000)
        if current_time - self.last_redraw_time > self.redraw_delay:
            self.canvas.destroy()
            self.canvas = tk.Canvas(self, bg="white", width=800, height=800)
            self.canvas.pack(fill=tk.BOTH, expand=True)
            self.info_label.destroy()
            self.info_label = tk.Label(self, text="", bg="lightyellow", bd=1, relief=tk.SOLID)

            # self.draw_coordinate_system()
            self.plot_points()
            self.draw_lines() if not self.tile_list else self.draw_lines(draw_from_tiles=True)
            self.canvas.bind("<ButtonPress-1>", self.on_press)
            self.canvas.bind("<B1-Motion>", self.on_drag)
            self.canvas.bind("<MouseWheel>", self.on_zoom)
            self.last_redraw_time = current_time
            print("Finished redrawing canvas")

    def get_coords_from_tiles(self, tile_list: list[Tile] = None, scaling: float = 1):
        _tiles = self.tile_list if not tile_list else tile_list

        coords = [(tile.x * scaling, tile.y * scaling) for tile in _tiles]
        return coords

    def plot_points(self):
        for x, y in self.coordinates:
            canvas_x = self.transform_x(x)
            canvas_y = self.transform_y(y)
            self.canvas.create_oval(
                canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill="red", tags="points")

    def draw_lines(self, draw_from_tiles: bool = False):
        if draw_from_tiles:
            if not self.tile_list:
                return

            for idx, tile in enumerate(self.tile_list[:-1]):
                cx1, cx2, cy1, cy2 = self._calc_canvas_coordinates(tile.x, tile.y,
                                                                   self.tile_list[idx + 1].x, self.tile_list[idx + 1].y)
                line_id = self.canvas.create_line(cx1, cx2, cy1, cy2, activewidth=5,
                                                  fill="blue", arrow=tk.LAST, tags="lines")
                self.canvas.tag_bind(line_id, "<Enter>", lambda event, _id=line_id: self.on_hover_enter(event, _id))
                self.canvas.tag_bind(line_id, "<Leave>", lambda event, _id=line_id: self.on_hover_leave(event, _id))
                self.canvas.tag_bind(line_id, "<ButtonPress-1>",
                                     self.create_click_handler(tile, self.tile_list[idx + 1]))
            return

        for i in range(len(self.coordinates) - 1):
            x1, y1 = self.coordinates[i]
            x2, y2 = self.coordinates[i + 1]
            canvas_x1 = self.transform_x(x1)
            canvas_y1 = self.transform_y(y1)
            canvas_x2 = self.transform_x(x2)
            canvas_y2 = self.transform_y(y2)
            line_id = self.canvas.create_line(canvas_x1, canvas_y1, canvas_x2, canvas_y2, activewidth=5,
                                              fill="blue", arrow=tk.LAST, tags="lines")
            self.canvas.tag_bind(line_id, "<Enter>", lambda event, _id=line_id: self.on_hover_enter(event, _id))
            self.canvas.tag_bind(line_id, "<Leave>", lambda event, _id=line_id: self.on_hover_leave(event, _id))
            self.canvas.tag_bind(line_id, "<ButtonPress-1>", self.create_coord_click_handler(x1, y1, x2, y2))

    def transform_x(self, x):
        return 400 + (x + self.offset_x) * self.scale

    def transform_y(self, y):
        return 400 - (y + self.offset_y) * self.scale

    def on_press(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        delta_x = event.x - self.drag_data["x"]
        delta_y = event.y - self.drag_data["y"]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.offset_x += delta_x / self.scale
        self.offset_y -= delta_y / self.scale
        self._redraw_canvas()

    def on_zoom(self, event):
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale *= scale_factor
        self._redraw_canvas()

    def on_hover_enter(self, event, line_id):
        # print("entering hover")
        self.canvas.itemconfig(line_id, fill="red")

    def on_hover_leave(self, event, line_id):
        # print("exiting hover")
        self.canvas.itemconfig(line_id, fill="blue")

    def on_click(self, event, first_tile: Tile, second_tile: Tile):
        # print("On click event")
        distance = sqrt((second_tile.x - first_tile.x)**2 + (second_tile.y - first_tile.y)**2)
        info = f"Distance: {distance:.2f}\nBeats: {first_tile.get_tile_duration_in_beats():.2f}"
        self.info_label.config(text=info)
        self.info_label.place(x=event.x + 10, y=event.y + 10)

    def create_click_handler(self, first_tile: Tile, second_tile: Tile):
        return lambda event: self.on_click(event, first_tile, second_tile)

    def on_coord_click(self, event, x1, y1, x2, y2):
        distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        info = f"Point 1: ({x1}, {y1})\nPoint 2: ({x2}, {y2})\nDistance: {distance:.2f}"
        self.info_label.config(text=info)
        self.info_label.place(x=event.x + 10, y=event.y + 10)

    def create_coord_click_handler(self, x1, y1, x2, y2):
        return lambda event: self.on_coord_click(event, x1, y1, x2, y2)
