PYGAME_FLAG = True
try:
    import pygame
except ImportError:
    PYGAME_FLAG = False

# Initialize Pygame
if PYGAME_FLAG:
    pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BG_COLOR = (30, 30, 30)
TILE_COLOR = (200, 200, 200)
ARROW_COLORS = {
    0: (255, 0, 0),
    1: (0, 0, 255),
    2: (0, 255, 0)
    }
ARROW_COUNT = 0
TILE_SIZE = 20  # Smaller tile size
FONT_SIZE = 20
OFFSET_AMOUNT = 10  # Offset amount for overlapping arrows
OFFSET_RANGE = (-10, 10)
TWIRL_TILE_COLOR = (0, 255, 255)
SPEED_CHANGE_COLOR = (255, 255, 0)

# Create the screen
if PYGAME_FLAG:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ADOFAI Map Viewer")
    font = pygame.font.Font(None, FONT_SIZE)


def map_angle_to_offset(angle):
    # Figure out how 'wide' each range is
    span = 360
    if OFFSET_RANGE[0] < 0:
        offset_span = (OFFSET_RANGE[0] + abs(OFFSET_RANGE[0]), OFFSET_RANGE[1] + abs(OFFSET_RANGE[0]))
    else:
        offset_span = (OFFSET_RANGE[0], OFFSET_RANGE[1])

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(angle) / float(span)

    # Convert the 0-1 range into a value in the right range.
    return OFFSET_RANGE[0] + (value_scaled * offset_span[1])


def draw_tile(tile):
    """Draw a single tile on the screen."""
    events = [None, None]
    if "Twirl" in tile.actions:
        events[0] = 1
    if "SetSpeed" in tile.actions:
        events[1] = 1
    if all(events):
        tile_color = (255, 255, 255)
    elif events[0]:
        tile_color = TWIRL_TILE_COLOR
    elif events[1]:
        tile_color = SPEED_CHANGE_COLOR

    else:
        tile_color = (0, 0, 0)
    x, y = tile.offset_x, tile.offset_y
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, tile_color, rect)


def draw_arrow(start_tile, end_tile, thickness: int,  offset_vector):
    """Draw an arrow from start_tile to end_tile."""
    global ARROW_COUNT
    arrow_color = ARROW_COLORS[start_tile.floor % 3]
    start_pos = pygame.math.Vector2(start_tile.offset_x + TILE_SIZE // 2,
                                    start_tile.offset_y + TILE_SIZE // 2) + offset_vector
    end_pos = pygame.math.Vector2(end_tile.offset_x + TILE_SIZE // 2,
                                  end_tile.offset_y + TILE_SIZE // 2) + offset_vector
    pygame.draw.line(screen, arrow_color, start_pos, end_pos, thickness)
    draw_arrowhead(end_pos, start_pos, arrow_color, thickness)
    ARROW_COUNT += 1


def draw_arrowhead(start_pos, end_pos, color, thickness):
    """Draw arrowhead at the end of an arrow line."""
    arrow_length = 10
    arrow_width = 5
    angle = pygame.math.Vector2(end_pos) - pygame.math.Vector2(start_pos)
    angle = pygame.math.Vector2.normalize(angle)
    arrow_point1 = end_pos - angle.rotate(135) * arrow_length
    arrow_point2 = end_pos - angle.rotate(-135) * arrow_length
    pygame.draw.polygon(screen, color, [start_pos, arrow_point1, arrow_point2], width=thickness)


def is_hovering_over_arrow(mouse_pos, start_tile, end_tile, offset_vector=None):
    """Check if the mouse is hovering over the arrow."""
    if offset_vector is None:
        offset_vector = pygame.math.Vector2(0, 0)
    start_pos = pygame.math.Vector2(start_tile.offset_x + TILE_SIZE // 2,
                                    start_tile.offset_y + TILE_SIZE // 2) + offset_vector
    end_pos = pygame.math.Vector2(end_tile.offset_x + TILE_SIZE // 2,
                                  end_tile.offset_y + TILE_SIZE // 2) + offset_vector
    arrow_vector = end_pos - start_pos
    mouse_vector = pygame.math.Vector2(mouse_pos) - start_pos
    projection_length = mouse_vector.dot(arrow_vector) / arrow_vector.length()
    projection_vector = projection_length * arrow_vector.normalize()
    nearest_point = start_pos + projection_vector
    distance_to_mouse = nearest_point.distance_to(mouse_pos)
    return 0 <= projection_length <= arrow_vector.length() and distance_to_mouse <= 5


def draw_tooltip(text, mouse_pos):
    """Draw tooltip with text near the mouse position."""
    tooltip_surface = font.render(text, True, (255, 255, 255))
    screen.blit(tooltip_surface, (mouse_pos[0] + 10, mouse_pos[1] - 20))


def mirror_map_y(tiles, center_line):
    """Mirror the map on the x-axis relative to the center line."""
    for tile in tiles:
        tile.offset_y = 2 * center_line - tile.offset_y


def main(tiles):
    clock = pygame.time.Clock()
    running = True
    offset_x, offset_y = 0, 0  # To handle panning
    zoom = 1.0  # Zoom factor
    dragging = False
    drag_start_x, drag_start_y = 0, 0
    mouse_pos = pygame.mouse.get_pos()
    hover_tile_index = None
    center_line = SCREEN_HEIGHT // 2  # Center line for mirroring

    mirror_map_y(tiles, center_line)  # Mirror the map on the x-axis

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click to start dragging
                    dragging = True
                    drag_start_x, drag_start_y = event.pos
                elif event.button == 4:  # Scroll up to zoom in
                    # Calculate the world position of the center of the screen
                    screen_center_x = SCREEN_WIDTH / 2
                    screen_center_y = SCREEN_HEIGHT / 2
                    world_center_x = (screen_center_x - offset_x) / zoom
                    world_center_y = (screen_center_y - offset_y) / zoom

                    # Increase the zoom factor
                    zoom *= 1.1

                    # Recalculate the new offsets to keep the world center at the screen center
                    offset_x = screen_center_x - world_center_x * zoom
                    offset_y = screen_center_y - world_center_y * zoom
                elif event.button == 5:  # Scroll down to zoom out
                    # Calculate the world position of the center of the screen
                    screen_center_x = SCREEN_WIDTH / 2
                    screen_center_y = SCREEN_HEIGHT / 2
                    world_center_x = (screen_center_x - offset_x) / zoom
                    world_center_y = (screen_center_y - offset_y) / zoom

                    # Decrease the zoom factor
                    zoom /= 1.1

                    # Recalculate the new offsets to keep the world center at the screen center
                    offset_x = screen_center_x - world_center_x * zoom
                    offset_y = screen_center_y - world_center_y * zoom
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left click to stop dragging
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    dx = event.pos[0] - drag_start_x
                    dy = event.pos[1] - drag_start_y
                    offset_x += dx
                    offset_y += dy
                    drag_start_x, drag_start_y = event.pos

        # Clear the screen
        screen.fill(BG_COLOR)

        # Draw all tiles and arrows
        for i in range(len(tiles) - 1):
            tile = tiles[i]
            next_tile = tiles[i + 1]
            # Apply panning and zoom
            tile.offset_x = (tile.offset_x * zoom) + offset_x
            tile.offset_y = (tile.offset_y * zoom) + offset_y
            next_tile.offset_x = (next_tile.offset_x * zoom) + offset_x
            next_tile.offset_y = (next_tile.offset_y * zoom) + offset_y

            # Calculate offset vector for overlapping arrows
            # IDEA: Let offsets be unique to every angle.
            offset_vector = pygame.math.Vector2(0, 0)
            if i > 0 and tiles[i - 1] == next_tile:
                offset_vector = pygame.math.Vector2(map_angle_to_offset(tile.angle), 0).rotate(tile.angle)

            # Check if the mouse is hovering over this arrow
            if is_hovering_over_arrow(mouse_pos, tile, next_tile, offset_vector):
                draw_arrow(tile, next_tile, 10, offset_vector)
                hover_tile_index = i
            else:
                draw_arrow(tile, next_tile, 2, offset_vector)

            draw_tile(tile)

            # Reset offsets for correct behavior in next frame
            tile.offset_x = (tile.offset_x - offset_x) / zoom
            tile.offset_y = (tile.offset_y - offset_y) / zoom
            next_tile.offset_x = (next_tile.offset_x - offset_x) / zoom
            next_tile.offset_y = (next_tile.offset_y - offset_y) / zoom

        # Draw the last tile
        last_tile = tiles[-1]
        last_tile.offset_x = (last_tile.offset_x * zoom) + offset_x
        last_tile.offset_y = (last_tile.offset_y * zoom) + offset_y
        draw_tile(last_tile)
        last_tile.offset_x = (last_tile.offset_x - offset_x) / zoom
        last_tile.offset_y = (last_tile.offset_y - offset_y) / zoom

        # Draw tooltip if hovering over an arrow
        if hover_tile_index is not None:
            tile = tiles[hover_tile_index]
            tooltip_text = f"Duration: {tile.duration_in_beats:.2f} beats"
            draw_tooltip(tooltip_text, mouse_pos)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
