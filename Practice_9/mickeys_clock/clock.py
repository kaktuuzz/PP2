import pygame
import datetime
import os

class clock:
    def __init__(self, width, height):
        self.size = (width, height)
        self.clock_center = pygame.math.Vector2(width // 2, height // 2)

        base_path = os.path.dirname(os.path.abspath(__file__))
        images_path = os.path.join(base_path, "images")

        self.load_images(images_path)
        self.setup_hands(images_path)

    def load_images(self, path):
        self.background = pygame.image.load(os.path.join(path, "clock.png"))
        self.background = pygame.transform.scale(self.background, self.size)

        self.body = pygame.image.load(os.path.join(path, "mikkey.png")).convert_alpha()
        self.body = pygame.transform.scale(self.body, (380, 500))
        self.body_rect = self.body.get_rect(center=self.clock_center)

    def setup_hands(self, path):
        self.minute_hand = pygame.image.load(os.path.join(path, "hand_right_centered.png")).convert_alpha()
        self.minute_hand = pygame.transform.scale(self.minute_hand, (200, 300))

        self.second_hand = pygame.image.load(os.path.join(path, "hand_left_centered.png")).convert_alpha()
        self.second_hand = pygame.transform.scale(self.second_hand, (190, 280))

        self.minute_pivot = (
            self.minute_hand.get_width() // 2,
            self.minute_hand.get_height()
        )

        self.second_pivot = (
            self.second_hand.get_width() // 2,
            self.second_hand.get_height()
        )

    def rotate_around_point(self, surface, image, center, pivot, angle):
        rect = image.get_rect(topleft=(center[0] - pivot[0], center[1] - pivot[1]))
        offset = pygame.math.Vector2(center) - rect.center
        rotated_offset = offset.rotate(-angle)
        new_center = (center[0] - rotated_offset.x, center[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=new_center)
        surface.blit(rotated_image, rotated_rect)

    def get_angles(self):
        now = datetime.datetime.now()
        return -6 * now.minute, -6 * now.second

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.body, self.body_rect.topleft)
        minute_angle, second_angle = self.get_angles()
        self.rotate_around_point(surface, self.minute_hand, self.clock_center, self.minute_pivot, minute_angle)
        self.rotate_around_point(surface, self.second_hand, self.clock_center, self.second_pivot, second_angle)