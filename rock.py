import pygame

# Rock class and how it shows in game and collision


class Rock:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))

    def collides_with(self, player):
        self.rect.x, self.rect.y = self.x + 20, self.y + 20
        self.rect.width, self.rect.height = self.width - 10, self.height - 10
        return player.collides_with(self.rect)