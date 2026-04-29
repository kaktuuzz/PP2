import pygame
import math
import datetime
from tools import flood_fill

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    # Surface where all drawings are stored
    canvas = pygame.Surface((1000, 800))
    canvas.fill((255, 255, 255))

    # Font for the text tool
    font = pygame.font.SysFont('arial', 24)
    font_ui = pygame.font.SysFont('arial', 16)

    radius = 5
    mode = 'draw'   # draw, line, rect, circle, square, r_triangle, e_triangle, rhombus, fill, text, eraser
    color = (0, 0, 0)

    drawing = False
    start_pos = (0, 0)
    last_pos = None

    # For line/shape preview while dragging
    preview_pos = (0, 0)

    # For the text tool
    typing = False
    text_pos = (0, 0)
    text_input = ''

    """
    CONTROLS
    D = free draw (pencil)
    L = straight line
    C = circle
    T = rectangle
    S = square
    Q = right triangle
    W = equilateral triangle
    H = rhombus
    F = flood fill
    X = text tool
    E = eraser
    1 = small brush (2px)
    2 = medium brush (5px)
    3 = large brush (10px)
    Mouse wheel = brush size
    LMB = draw
    Ctrl+S = save as PNG
    """

    # Available colors list
    colors_list = [
        (0,   0,   0),      # black
        (255, 255, 255),    # white
        (220, 50,  50),     # red
        (50,  180, 50),     # green
        (50,  100, 220),    # blue
        (240, 200, 30),     # yellow
        (240, 130, 30),     # orange
        (160, 60,  220),    # purple
        (30,  210, 220),    # cyan
        (230, 80,  160),    # pink
        (140, 80,  30),     # brown
        (150, 150, 150),    # gray
    ]

    # Returns RGB for the current color
    def get_color():
        return color

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:

                # If the text tool is active, capture keyboard input
                if typing:
                    if event.key == pygame.K_RETURN:
                        # Draw the text onto the canvas and stop typing
                        text_surface = font.render(text_input, True, color)
                        canvas.blit(text_surface, text_pos)
                        typing = False
                        text_input = ''
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel text input
                        typing = False
                        text_input = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    else:
                        # Add the typed character if it's printable
                        if event.unicode and event.unicode.isprintable():
                            text_input += event.unicode
                    continue  # Don't process other keys while typing

                # Ctrl+S to save
                mods = pygame.key.get_mods()
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = 'canvas_' + timestamp + '.png'
                    pygame.image.save(canvas, filename)
                    pygame.display.set_caption('Paint - Saved: ' + filename)
                    continue

                # Drawing modes
                if event.key == pygame.K_d:
                    mode = 'draw'
                elif event.key == pygame.K_l:
                    mode = 'line'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_q:
                    mode = 'r_triangle'
                elif event.key == pygame.K_w:
                    mode = 'e_triangle'
                elif event.key == pygame.K_h:
                    mode = 'rhombus'
                elif event.key == pygame.K_f:
                    mode = 'fill'
                elif event.key == pygame.K_x:
                    mode = 'text'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # Brush sizes
                if event.key == pygame.K_1:
                    radius = 2
                elif event.key == pygame.K_2:
                    radius = 5
                elif event.key == pygame.K_3:
                    radius = 10

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if clicked on a color swatch at the bottom
                    mx, my = event.pos
                    if my > 760:
                        # Color bar is at y=765, each swatch is 30px wide
                        swatch_index = mx // 30
                        if swatch_index < len(colors_list):
                            color = colors_list[swatch_index]
                    else:
                        # Clicked on the canvas
                        drawing = True
                        start_pos = event.pos
                        last_pos = event.pos
                        preview_pos = event.pos

                        # Flood fill happens immediately on click
                        if mode == 'fill':
                            flood_fill(canvas, event.pos, color)
                            drawing = False

                        # Text tool places the cursor on click
                        if mode == 'text':
                            typing = True
                            text_pos = event.pos
                            text_input = ''
                            drawing = False

                elif event.button == 4:  # Scroll up - bigger brush
                    radius = min(50, radius + 1)

                elif event.button == 5:  # Scroll down - smaller brush
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    # STRAIGHT LINE
                    if mode == 'line':
                        pygame.draw.line(canvas, color, start_pos, end_pos, radius)

                    # RECTANGLE
                    elif mode == 'rect':
                        pygame.draw.rect(
                            canvas,
                            color,
                            pygame.Rect(start_pos,
                            (end_pos[0] - start_pos[0],
                             end_pos[1] - start_pos[1])),
                            radius
                        )

                    # SQUARE (equal sides)
                    elif mode == 'square':
                        side = min(abs(end_pos[0] - start_pos[0]),
                                   abs(end_pos[1] - start_pos[1]))
                        pygame.draw.rect(
                            canvas,
                            color,
                            pygame.Rect(start_pos, (side, side)),
                            radius
                        )

                    # CIRCLE
                    elif mode == 'circle':
                        r = int(((end_pos[0]-start_pos[0])**2 +
                                 (end_pos[1]-start_pos[1])**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, radius)

                    # RIGHT TRIANGLE
                    elif mode == 'r_triangle':
                        points = [
                            start_pos,
                            (start_pos[0], end_pos[1]),
                            end_pos
                        ]
                        pygame.draw.polygon(canvas, color, points, radius)

                    # EQUILATERAL TRIANGLE
                    elif mode == 'e_triangle':
                        side = abs(end_pos[0] - start_pos[0])
                        height = int((math.sqrt(3) / 2) * side)

                        p1 = start_pos
                        p2 = (start_pos[0] + side, start_pos[1])
                        p3 = (start_pos[0] + side // 2, start_pos[1] - height)

                        pygame.draw.polygon(canvas, color, [p1, p2, p3], radius)

                    # RHOMBUS
                    elif mode == 'rhombus':
                        mid_x = (start_pos[0] + end_pos[0]) // 2
                        mid_y = (start_pos[1] + end_pos[1]) // 2

                        points = [
                            (mid_x, start_pos[1]),   # top
                            (end_pos[0], mid_y),     # right
                            (mid_x, end_pos[1]),     # bottom
                            (start_pos[0], mid_y)    # left
                        ]
                        pygame.draw.polygon(canvas, color, points, radius)

            if event.type == pygame.MOUSEMOTION:
                preview_pos = event.pos

                if drawing:
                    if mode == 'draw':
                        if last_pos is not None:
                            pygame.draw.line(
                                canvas,
                                color,
                                last_pos,
                                event.pos,
                                radius * 2
                            )
                        last_pos = event.pos

                    elif mode == 'eraser':
                        pygame.draw.circle(canvas, (255, 255, 255),
                                           event.pos, radius * 3)

        # Draw the canvas onto the screen
        screen.blit(canvas, (0, 0))

        # Draw a live preview of the shape while the user is dragging
        if drawing and mode in ('line', 'rect', 'square', 'circle', 'r_triangle', 'e_triangle', 'rhombus'):
            end_pos = preview_pos

            if mode == 'line':
                pygame.draw.line(screen, color, start_pos, end_pos, radius)

            elif mode == 'rect':
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(start_pos,
                    (end_pos[0] - start_pos[0],
                     end_pos[1] - start_pos[1])),
                    radius
                )

            elif mode == 'square':
                side = min(abs(end_pos[0] - start_pos[0]),
                           abs(end_pos[1] - start_pos[1]))
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(start_pos, (side, side)),
                    radius
                )

            elif mode == 'circle':
                r = int(((end_pos[0]-start_pos[0])**2 +
                         (end_pos[1]-start_pos[1])**2) ** 0.5)
                if r > 0:
                    pygame.draw.circle(screen, color, start_pos, r, radius)

            elif mode == 'r_triangle':
                points = [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ]
                pygame.draw.polygon(screen, color, points, radius)

            elif mode == 'e_triangle':
                side = abs(end_pos[0] - start_pos[0])
                if side > 0:
                    height = int((math.sqrt(3) / 2) * side)
                    p1 = start_pos
                    p2 = (start_pos[0] + side, start_pos[1])
                    p3 = (start_pos[0] + side // 2, start_pos[1] - height)
                    pygame.draw.polygon(screen, color, [p1, p2, p3], radius)

            elif mode == 'rhombus':
                mid_x = (start_pos[0] + end_pos[0]) // 2
                mid_y = (start_pos[1] + end_pos[1]) // 2
                points = [
                    (mid_x, start_pos[1]),
                    (end_pos[0], mid_y),
                    (mid_x, end_pos[1]),
                    (start_pos[0], mid_y)
                ]
                pygame.draw.polygon(screen, color, points, radius)

        # Show live text preview while typing
        if typing:
            preview_text = font.render(text_input + '|', True, color)
            screen.blit(preview_text, text_pos)

        # Draw the color bar at the bottom
        for i, c in enumerate(colors_list):
            pygame.draw.rect(screen, c, pygame.Rect(i * 30, 765, 28, 28))
            # Highlight the currently selected color
            if c == color:
                pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(i * 30, 765, 28, 28), 2)

        # Draw a small UI bar at the top showing current mode, brush size
        pygame.draw.rect(screen, (30, 30, 30), pygame.Rect(0, 0, 1000, 22))

        mode_text = font_ui.render('Mode: ' + mode + '   Brush: ' + str(radius) + 'px   [D]raw [L]ine [C]ircle [T]rect [S]quare [Q]rtri [W]etri [H]rhombus [F]ill [X]text [E]raser   Ctrl+S=Save', True, (200, 200, 200))
        screen.blit(mode_text, (5, 3))

        pygame.display.flip()
        clock.tick(60)

main()