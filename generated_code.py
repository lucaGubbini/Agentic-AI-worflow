import sys
import pygame
import random

# Initializing Pygame
pygame.init()

# Setting up some constants
WIDTH = 640
HEIGHT = 480
FPS = 10

# Creating the display screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Defining colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Creating the snake and its initial position
snake_positions = [[(WIDTH / 2), (HEIGHT / 2)]]
direction = [1, 0]

# Setting up the font for score display
font = pygame.font.Font(None, 36)

# Game clock
clock = pygame.time.Clock()
score = 0
food_pos = []
game_over = False

while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = [-1, 0]
            elif event.key == pygame.K_DOWN:
                direction = [1, 0]
            elif event.key == pygame.K_LEFT:
                direction = [0, -1]
            elif event.key == pygame.K_RIGHT:
                direction = [0, 1]

    # Updating the snake's position
    head_pos = snake_positions[-1][0] + direction[0]
    new_snake_position = []

    for pos in snake_positions[:-1]:
        if pos == (head_pos, snake_positions[-1][1]):
            game_over = True
            break

    if not game_over:
        new_snake_position.append(snake_positions[-1])
        snake_positions.append((head_pos, snake_positions[-1][0], snake_positions[-1][1]))

        # Checking for food collision
        if head_pos == food_pos:
            score += 10
            food_pos = None
            while not food_pos:
                food_pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]

    # Clearing the screen
    screen.fill(BLACK)

    # Drawing the snake
    for pos in snake_positions:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 20, 20))

    # Drawing the food
    if food_pos is not None:
        pygame.draw.circle(screen, RED, food_pos, 5)

    # Displaying the score
    label = font.render("Score: " + str(score), True, WHITE)
    screen.blit(label, (10, 10))

    pygame.display.flip()

    # Setting the frame rate
    clock.tick(FPS)