import pygame
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()

    # Surface where all drawings are stored
    canvas = pygame.Surface((1000, 800))
    canvas.fill((0, 0, 0))

    radius = 5
    mode = 'draw'   # draw, rect, circle, square, r_triangle, e_triangle, rhombus, eraser
    color_mode = 'blue'

    drawing = False
    start_pos = (0, 0)
    last_pos = None

    """
    CONTROLS
    B / R / G = Colors
    D = free draw
    C = circle
    T = rectangle
    S = square
    Q = right triangle
    W = equilateral triangle
    H = rhombus
    E = eraser
    Mouse wheel = brush size
    LMB = draw
    """

    # Returns RGB color based on selected mode
    def get_color():
        if color_mode == 'blue':
            return (0, 0, 255)
        elif color_mode == 'red':
            return (255, 0, 0)
        elif color_mode == 'green':
            return (0, 255, 0)
        return (255, 255, 255)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Drawing modes
                if event.key == pygame.K_d:
                    mode = 'draw'
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
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # Color selection
                if event.key == pygame.K_r:
                    color_mode = 'red'
                elif event.key == pygame.K_g:
                    color_mode = 'green'
                elif event.key == pygame.K_b:
                    color_mode = 'blue'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

                elif event.button == 4:  # Scroll up
                    radius = min(50, radius + 1)

                elif event.button == 5:  # Scroll down
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    color = get_color()

                    # RECTANGLE
                    if mode == 'rect':
                        pygame.draw.rect(
                            canvas,
                            color,
                            pygame.Rect(start_pos,
                            (end_pos[0] - start_pos[0],
                             end_pos[1] - start_pos[1])),
                            2
                        )

                    # SQUARE (equal sides)
                    elif mode == 'square':
                        side = min(abs(end_pos[0] - start_pos[0]),
                                   abs(end_pos[1] - start_pos[1]))
                        pygame.draw.rect(
                            canvas,
                            color,
                            pygame.Rect(start_pos, (side, side)),
                            2
                        )

                    # CIRCLE
                    elif mode == 'circle':
                        r = int(((end_pos[0]-start_pos[0])**2 +
                                 (end_pos[1]-start_pos[1])**2) ** 0.5)
                        pygame.draw.circle(canvas, color, start_pos, r, 2)

                    # RIGHT TRIANGLE
                    elif mode == 'r_triangle':
                        points = [
                            start_pos,
                            (start_pos[0], end_pos[1]),
                            end_pos
                        ]
                        pygame.draw.polygon(canvas, color, points, 2)

                    # EQUILATERAL TRIANGLE
                    elif mode == 'e_triangle':
                        side = abs(end_pos[0] - start_pos[0])
                        height = int((math.sqrt(3) / 2) * side)

                        p1 = start_pos
                        p2 = (start_pos[0] + side, start_pos[1])
                        p3 = (start_pos[0] + side // 2, start_pos[1] - height)

                        pygame.draw.polygon(canvas, color, [p1, p2, p3], 2)

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
                        pygame.draw.polygon(canvas, color, points, 2)

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    if mode == 'draw':
                        if last_pos is not None:
                            pygame.draw.line(
                                canvas,
                                get_color(),
                                last_pos,
                                event.pos,
                                radius * 2
                            )
                        last_pos = event.pos

                    elif mode == 'eraser':
                        pygame.draw.circle(canvas, (0, 0, 0),
                                           event.pos, radius)

        # Display the canvas
        screen.blit(canvas, (0, 0))
        pygame.display.flip()
        clock.tick(60)

main()