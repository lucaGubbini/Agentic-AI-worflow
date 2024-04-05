import sys
import pygame
import random

pygame.init()
win = pygame.display.set_mode((350, 420))
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

width, height = 35, 35
block_size = 10
snake_speed = 10

class snake():
    def __init__(self):
        self.length = 1
        self.x = [width * 2, width]
        self.y = [height * 2, height]
        self.direction = 'right'
        self.velocity = [snake_speed, 0]

    def move(self):
        if self.direction == 'up':
            self.velocity = [-snake_speed, snake_speed]
        elif self.direction == 'down':
            self.velocity = [snake_speed, snake_speed]
        elif self.direction == 'left':
            self.velocity = [-snake_speed, -snake_speed]
        elif self.direction == 'right':
            self.velocity = [snake_speed, -snake_speed]

        new_head = [self.x[0] + self.velocity[0], self.y[0] + self.velocity[1]]
        if not self.collide(new_head):
            self.x.insert(0, new_head[0])
            self.y.insert(0, new_head[1])

    def collide(self, pos):
        for x in self.x[1:]:
            if pos == (x, y):
                return True
        return False

def game_loop():
    snake = snake()
    food = Food()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != 'down':
                    snake.direction = 'up'
                elif event.key == pygame.K_DOWN and snake.direction != 'up':
                    snake.direction = 'down'
                elif event.key == pygame.K_LEFT and snake.direction != 'right':
                    snake.direction = 'left'
                elif event.key == pygame.K_RIGHT and snake.direction != 'left':
                    snake.direction = 'right'

        snake.move()
        win.fill((255, 0, 0))
        pygame.draw.rect(win, (0, 255, 0), (food.x, food.y, block_size, block_size))

        for x in snake.x:
            pygame.draw.rect(win, (0, 255, 0), (x, y, width, height))

        pygame.display.flip()
        clock.tick(60)

class Food():
    def __init__(self):
        self.x = random.randint(0, int((win.get_width() / block_size) * (block_size)))
        self.y = random.randint(0, int((win.get_height() / block_size) * (block_size)))

    def spawn(self):
        while pygame.sprite.Group().colliderect(self, snake):
            self.__init__()

game_loop()