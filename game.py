import pygame
import sys
import random
from enemy import Enemy
from player import Player
from rock import Rock

# Initial Game Info
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Catalina Kayak Adventure")
clock = pygame.time.Clock()

# Loading Player Image and Flipping Kayak

player_image = pygame.image.load("kayak.png").convert_alpha()
player_image = pygame.transform.flip(player_image, True, False)
player_width, player_height = 100,  100
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Loading Enemy and Rock Images and setting their size

shark_image = pygame.image.load("shark.png").convert_alpha()
crab_image = pygame.image.load("crab.png").convert_alpha()
whale_image = pygame.image.load("whale.png").convert_alpha()
rock_image = pygame.image.load("rock.png").convert_alpha()

scaled_shark_width, scaled_shark_height = 200, 150
scaled_crab_width, scaled_crab_height = 200, 150
scaled_whale_width, scaled_whale_height = 200, 150
scaled_rock_width, scaled_rock_height = 100, 100


shark_image = pygame.transform.scale(shark_image, (scaled_shark_width, scaled_shark_height))
crab_image = pygame.transform.scale(crab_image, (scaled_crab_width, scaled_crab_height))
whale_image = pygame.transform.scale(whale_image, (scaled_whale_width, scaled_whale_height))
rock_image = pygame.transform.scale(rock_image, (scaled_rock_width, scaled_rock_height))

# Creating the world map

world_width = 5000
world_height = 2400
water_height = 1800
land_height = world_height - water_height


# Creating Enemy in game movement


def create_enemy():
    enemy_x = random.randint(800, world_width - max(scaled_shark_width, scaled_crab_width, scaled_whale_width))
    enemy_y = random.randint(0, water_height - max(scaled_shark_height, scaled_crab_height, scaled_whale_height))
    enemy_image, enemy_type = random.choice([(shark_image, 1), (crab_image, 2), (whale_image, 3)])
    speed_x = random.randint(2, 7)
    speed_y = random.randint(-2, 2)
    new_enemy = Enemy(enemy_x, enemy_y, enemy_image, speed_x, speed_y, enemy_type)
    return new_enemy

# Setting how the enemy will spawn


def spawn_enemy():
    new_enemy = create_enemy()
    enemies.append(new_enemy)

# Spawning the rocks in game


def generate_rock():
    rock_x = random.randint(800, world_width - scaled_rock_width)
    rock_y = random.randint(0, water_height - scaled_rock_height)
    new_rock = Rock(rock_x, rock_y, rock_image)
    return new_rock


# Checking if player made it to the other island


def check_for_level_completion(player, world_width):
    if player.x + player.width > world_width - 680:
        return True
    return False

# Displaying messages in game


def display_message(message, size, x, y, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    text = font.render(message, True, color)
    screen.blit(text, (x, y))

# Start Screen before game begins


def start_screen():
    screen.fill((0, 128, 255))
    display_message("Welcome to Catalina Kayak Adventure!", 55, 30, 200)
    display_message("- Use your arrow keys to get to the other island safely!", 27, 140, 250)
    display_message("- Avoid rocks and sea creatures!", 27, 230, 280)
    display_message("Press 'Enter' to Start the Game.", 40, 190, 350)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


player = Player(400, 550, 40, 60, player_image)
enemies = []
enemy_frequency = 800
level = 1
start_screen()


# Main game loop

def game_loop():
    global level, enemy_frequency, enemies
    player.x = 400
    player.y = 550
    camera_x = player.x - 400
    camera_y = player.y - 300
    rocks = [generate_rock() for _ in range(50)]

    last_enemy_added = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()

        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (0, 128, 255), (0, 0, world_width - camera_x, water_height - camera_y))  # Water
        pygame.draw.rect(screen, (194, 178, 128), (0, 0, 400 - camera_x, world_height - camera_y))  # Left land
        pygame.draw.rect(screen, (194, 178, 128), (world_width - 600 - camera_x, 0, 600, world_height - camera_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        player.move(keys)
        camera_x = player.x - 400
        camera_y = min(max(player.y - 300, 0), water_height - 600)

        if current_time - last_enemy_added > enemy_frequency:
            spawn_enemy()
            last_enemy_added = current_time

        player.keep_within_bounds(water_height, world_width)

        game_over = False
        for enemy in enemies:
            enemy.move()
            if enemy.collides_with(player):
                game_over = True
                break
            enemy.draw(screen, camera_x, camera_y)

        for rock in rocks:
            rock.draw(screen, camera_x, camera_y)
            if rock.collides_with(player):
                game_over = True
                break

# Message displayed if player collides, also resets level counter

        if game_over:
            display_message("Game Over! Press 'Space' to restart or ESC to quit.", 40, 50, 300)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            if level >= 1:
                                level = 1
                            game_loop()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        player.draw(screen, camera_x, camera_y)
        camera_x = player.x - 400
        camera_y = player.y - 300

# Displays players current level, and message when they reach other island

        display_message(f"Level: {level}", 30, 10, 10)

        if check_for_level_completion(player, world_width):
            display_message("Level complete! Press 'Enter' to Continue.", 50, 100, 300)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            level += 1
                            game_loop()
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()

        clock.tick(60)


game_loop()