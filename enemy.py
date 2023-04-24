import math
import random
import pygame


# Enemy class that shows how it is shown in game, how the enemies move, and how they collide

class Enemy:
    def __init__(self, x, y, image, speed_x, speed_y, enemy_type):
        self.x = x
        self.y = y
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.enemy_type = enemy_type
        self.direction_change_frequency = 1000
        self.last_direction_change = pygame.time.get_ticks()

    def change_direction(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_direction_change >= self.direction_change_frequency:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
            self.last_direction_change = current_time

    def move(self):
        if self.enemy_type == 1:
            self.x += self.speed_x
        elif self.enemy_type == 2:
            if self.direction == 'left':
                self.x -= self.speed_x
            elif self.direction == 'right':
                self.x += self.speed_x
            elif self.direction == 'up':
                self.y -= self.speed_y
            elif self.direction == 'down':
                self.y += self.speed_y
            self.change_direction()
        elif self.enemy_type == 3:
            self.x += int(self.speed_x * math.cos(self.speed_y))
            self.y += int(self.speed_x * math.sin(self.speed_y))
            self.speed_y += 0.05

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))

    def is_off_screen(self):
        return self.x + self.width < 0

    def collides_with(self, player):
        self.rect.x, self.rect.y = self.x + 10, self.y + 10
        self.rect.width, self.rect.height = self.width - 20, self.height - 20
        return player.collides_with(self.rect)