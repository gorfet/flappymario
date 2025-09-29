import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and scale images
bird_image = pygame.image.load('bird.png')
coin_image = pygame.image.load('coin.png')
pipe_image = pygame.image.load('pipe.png')

# Scale characters (adjust these values to taste)
BIRD_WIDTH, BIRD_HEIGHT = 50, 35
PIPE_WIDTH, PIPE_HEIGHT = 80, 500

bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))

# Game setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Mari')
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 48)
big_font = pygame.font.SysFont(None, 72)


# Function to create pipes
def create_pipe():
    height = random.randint(150, 400)
    top_pipe = pipe_image.get_rect(midbottom=(SCREEN_WIDTH, height - PIPE_GAP // 2))
    bottom_pipe = pipe_image.get_rect(midtop=(SCREEN_WIDTH, height + PIPE_GAP // 2))
    return top_pipe, bottom_pipe


# Draw score
def draw_score(score):
    text = font.render(str(score), True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2, 50))


# Start screen
def start_screen():
    screen.fill(WHITE)
    title_text = big_font.render("FLAPPY MARIO  ", True, BLACK)
    instruction_text = font.render("Press SPACE to Start", True, BLACK)

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2,
                             SCREEN_HEIGHT // 2 - 100))
    screen.blit(instruction_text, (SCREEN_WIDTH // 2 - instruction_text.get_width() // 2,
                                   SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# Game over screen
def game_over_screen():
    game_over_text = big_font.render("GAME OVER", True, BLACK)
    restart_text = font.render("Press SPACE to Restart", True, BLACK)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                 SCREEN_HEIGHT // 2 - 100))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                               SCREEN_HEIGHT // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


# Run one round of the game
def play_game():
    bird_rect = bird_image.get_rect(center=(100, SCREEN_HEIGHT // 2))
    bird_velocity = 0
    pipes = []
    score = 0

    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQUENCY)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH
            if event.type == pygame.USEREVENT:
                pipes.extend(create_pipe())

        # Bird movement
        bird_velocity += GRAVITY
        bird_rect.centery += bird_velocity

        # Move pipes
        new_pipes = []
        for pipe in pipes:
            pipe.centerx -= 5
            if pipe.right > 0:
                new_pipes.append(pipe)
        pipes = new_pipes

        # Check for scoring
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx and pipe.bottom > SCREEN_HEIGHT // 2:
                score += 1

        # Drawing
        screen.fill(WHITE)
        screen.blit(bird_image, bird_rect)
        for pipe in pipes:
            if pipe.bottom > SCREEN_HEIGHT // 2:  # bottom pipe
                screen.blit(pipe_image, pipe)
            else:  # top pipe flipped
                flipped_pipe = pygame.transform.flip(pipe_image, False, True)
                screen.blit(flipped_pipe, pipe)

        draw_score(score)

        # Check for collisions
        for pipe in pipes:
            if bird_rect.colliderect(pipe):
                return  # end round

        if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
            return  # end round

        pygame.display.flip()
        clock.tick(60)


# Main game loop (with start + restart screens)
def main():
    while True:
        start_screen()
        play_game()
        game_over_screen()


if __name__ == "__main__":
    main()
