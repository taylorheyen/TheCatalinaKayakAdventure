import pygame


# Player class for movement, and collision detection

class Player:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel_x = 0
        self.vel_y = 0
        self.health = 100
        self.image = image

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 5
        else:
            self.vel_x = 0

        if keys[pygame.K_UP]:
            self.vel_y = -5
        elif keys[pygame.K_DOWN]:
            self.vel_y = 5
        else:
            self.vel_y = 0

        self.x += self.vel_x
        self.y += self.vel_y

    def keep_within_bounds(self, water_height, world_width):
        self.x = max(400, min(self.x, world_width - 600 - self.width))
        self.y = max(0, min(self.y, water_height - self.height))

    def collides_with(self, other_rect):
        player_rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)
        return player_rect.colliderect(other_rect)