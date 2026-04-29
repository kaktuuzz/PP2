import pygame
from collections import deque


# Flood fill tool - fills an area with the chosen color
def flood_fill(canvas, pos, fill_color):
    x, y = pos
    width = canvas.get_width()
    height = canvas.get_height()

    # Don't do anything if click is outside the canvas
    if x < 0 or x >= width or y < 0 or y >= height:
        return

    # Get the color we clicked on
    target_color = canvas.get_at((x, y))[:3]

    # If it's already the same color, nothing to do
    if target_color == fill_color:
        return

    # Use a queue to spread the fill (BFS)
    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        # Skip if out of bounds
        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue

        # Skip if this pixel is not the color we're replacing
        if canvas.get_at((cx, cy))[:3] != target_color:
            continue

        # Paint this pixel
        canvas.set_at((cx, cy), fill_color)

        # Add neighbors
        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))