import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
GRAVITY = 3
JUMP_STRENGTH =50 # Adjust this value for a stronger jump
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Import fonts
pygame.font.init()

# Font settings
FONT = pygame.font.SysFont("calibri", 50)

# Player class
class Player:
    def __init__(self):
        self.x = WIDTH // 4
        self.y = HEIGHT - PLAYER_SIZE
        self.velocity = 0
        self.color = GREEN
        self.score = 0

    def jump(self):
        if self.y == HEIGHT - PLAYER_SIZE:
            self.velocity = -JUMP_STRENGTH

    def update(self):
        self.y += self.velocity
        self.velocity += GRAVITY

        # Keep the player on the ground
        if self.y > HEIGHT - PLAYER_SIZE:
            self.y = HEIGHT - PLAYER_SIZE
            self.velocity = 0

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, int(self.y), PLAYER_SIZE, PLAYER_SIZE))

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = WIDTH
        self.y = HEIGHT - PLAYER_SIZE
        self.width = 30
        self.color = RED

    def update(self, speed):
        # Adjust the value by which obstacles move to change their speed
        self.x -= speed

    def off_screen(self):
        return self.x + self.width < 0

    def render(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, int(self.y), self.width, PLAYER_SIZE))

def show_new_game_message(surface):
    new_game_text = FONT.render("New Game", True, WHITE)
    new_game_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    pygame.draw.rect(surface, WHITE, new_game_button_rect, 2)
    surface.blit(new_game_text, (new_game_button_rect.centerx - new_game_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)  # Display the message for 2 seconds

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()

    player = Player()
    obstacles = []

    show_new_game_message(surface)

    game_over = False
    new_game_delay = 3  # Delay before starting a new game (in seconds)
    speed_increase_time = time.time() + 5  # Increase speed every 5 seconds
    speed = 5  # Initial speed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                if new_game_button_rect.collidepoint(event.pos):
                    player = Player()
                    obstacles = []
                    game_over = False
                    speed_increase_time = time.time() + 5

        if not game_over:
            player.update()

            # Check if it's time to increase speed
            if time.time() >= speed_increase_time:
                speed += 2  # Increase speed by 2 units
                speed_increase_time = time.time() + 5  # Reset the timer

            # Adjust the number in random.randint to change the frequency of obstacle creation
            if random.randint(1, 100) == 1:
                obstacles.append(Obstacle())

            for obstacle in obstacles:
                obstacle.update(speed)

            obstacles = [obstacle for obstacle in obstacles if not obstacle.off_screen()]

            for obstacle in obstacles:
                if (
                    player.x < obstacle.x + obstacle.width
                    and player.x + PLAYER_SIZE > obstacle.x
                    and player.y < obstacle.y + PLAYER_SIZE
                    and player.y + PLAYER_SIZE > obstacle.y
                ):
                    game_over = True

            player.score += 1

            surface.fill((0, 0, 0))
            player.render(surface)

            for obstacle in obstacles:
                obstacle.render(surface)

            # Display score
            score_text = FONT.render(f"Score: {player.score}", True, WHITE)
            surface.blit(score_text, (10, 10))

        if game_over:
            game_over_text = FONT.render("Game Over", True, WHITE)
            surface.blit(game_over_text, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 50))
            score_text = FONT.render(f"Score: {player.score}", True, WHITE)
            surface.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 + 50))

            new_game_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
            pygame.draw.rect(surface, WHITE, new_game_button_rect, 2)
            new_game_text = FONT.render("New Game", True, WHITE)
            surface.blit(new_game_text, (new_game_button_rect.centerx - new_game_text.get_width() // 2, HEIGHT // 2))

        screen.blit(surface, (0, 0))
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
