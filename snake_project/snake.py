import pygame
import random


pygame.init()


WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")


WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

UP = (0, -GRID_SIZE)
DOWN = (0, GRID_SIZE)
LEFT = (-GRID_SIZE, 0)
RIGHT = (GRID_SIZE, 0)

class Snake:
    def __init__(self, color, start_pos):
        self.body = [start_pos]
        self.direction = RIGHT
        self.growing = False
        self.alive = True
        self.color = color
        self.score = 0
        self.lives = 3  

    def move(self):
        if not self.alive:
            return
        head = (self.body[0][0] + self.direction[0], self.body[0][1] + self.direction[1])
        if head in self.body or head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT:
            self.lives -= 1
            if self.lives > 0:
                self.body = [(WIDTH // 2, HEIGHT // 2)]
                self.direction = RIGHT
            else:
                self.alive = False
        else:
            self.body.insert(0, head)
            if not self.growing:
                self.body.pop()
            self.growing = False

    def grow(self):
        self.growing = True

    def change_direction(self, new_direction):
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def draw(self, screen):
        for part in self.body:
            pygame.draw.rect(screen, self.color, (*part, GRID_SIZE, GRID_SIZE))

class Apple:
    def __init__(self):
        self.position = self.spawn()

    def spawn(self):
        return (random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE,
                random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (*self.position, GRID_SIZE, GRID_SIZE))


def game_loop():
    clock = pygame.time.Clock()
    snake1 = Snake(GREEN, (WIDTH // 4, HEIGHT // 2))
    snake2 = Snake(BLUE, (3 * WIDTH // 4, HEIGHT // 2))  
    apple = Apple()

    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_UP:
                    snake1.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake1.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake1.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake1.change_direction(RIGHT)
                
                elif event.key == pygame.K_w:
                    snake2.change_direction(UP)
                elif event.key == pygame.K_s:
                    snake2.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    snake2.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    snake2.change_direction(RIGHT)

        snake1.move()
        snake2.move()

    
        for snake in [snake1, snake2]:
            if snake.body[0] == apple.position:
                snake.grow()
                snake.score += 1
                apple.position = apple.spawn()

                
                if snake.score % 25 == 0:
                    snake.lives += 1

        snake1.draw(screen)
        snake2.draw(screen)
        apple.draw(screen)

        font = pygame.font.Font(None, 24)
        score_text = font.render(f"Punkty: {snake1.score} | Życia: {snake1.lives}", True, GREEN)
        score_text2 = font.render(f"Punkty: {snake2.score} | Życia: {snake2.lives}", True, BLUE)
        screen.blit(score_text, (10, 10))
        screen.blit(score_text2, (10, 30))

        if not snake1.alive and not snake2.alive:
            game_over(screen, snake1, snake2)
            running = False

        pygame.display.flip()
        clock.tick(10)

def game_over(screen, snake1, snake2):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    text = font.render("Koniec gry! Wyniki:", True, RED)
    score_text1 = font.render(f"Gracz 1: {snake1.score} punktów", True, GREEN)
    score_text2 = font.render(f"Gracz 2: {snake2.score} punktów", True, BLUE)
    restart_text = font.render("Naciśnij R, aby zagrać ponownie", True, (0, 0, 0))
    screen.blit(text, (WIDTH // 4, HEIGHT // 4))
    screen.blit(score_text1, (WIDTH // 4, HEIGHT // 3))
    screen.blit(score_text2, (WIDTH // 4, HEIGHT // 3 + 30))
    screen.blit(restart_text, (WIDTH // 4, HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                    waiting = False

game_loop()
pygame.quit()