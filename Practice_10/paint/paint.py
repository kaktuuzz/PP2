import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    # drawing surface (important!)
    canvas = pygame.Surface((640, 480))
    canvas.fill((0, 0, 0))

    radius = 5
    mode = 'draw'   # draw, rect, circle, eraser
    color_mode = 'blue'

    drawing = False
    start_pos = (0, 0)
    last_pos = None

    """
    CONTROLS
    B / R / G = Colors
    D = draw mode
    C = circle
    T = rectangle
    E = eraser
    Mouse wheel = brush size
    LMB = draw
    """

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
                # modes
                if event.key == pygame.K_d:
                    mode = 'draw'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

                # colors
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
                    last_pos = event.pos  # start new stroke

                elif event.button == 4:  # scroll up
                    radius = min(50, radius + 1)

                elif event.button == 5:  # scroll down
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    end_pos = event.pos

                    if mode == 'rect':
                        pygame.draw.rect(
                            canvas,
                            get_color(),
                            pygame.Rect(
                                start_pos,
                                (end_pos[0] - start_pos[0],
                                 end_pos[1] - start_pos[1])
                            ),
                            2
                        )

                    elif mode == 'circle':
                        center = start_pos
                        r = int(((end_pos[0]-start_pos[0])**2 +
                                 (end_pos[1]-start_pos[1])**2) ** 0.5)
                        pygame.draw.circle(canvas, get_color(), center, r, 2)

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

        # draw canvas to screen
        screen.blit(canvas, (0, 0))

        pygame.display.flip()
        clock.tick(60)


main()