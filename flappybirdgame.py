import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 400, 600
BIRD_X, BIRD_Y = 50, HEIGHT // 2
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Bird
bird = pygame.Rect(BIRD_X, BIRD_Y, 30, 30)
bird_velocity = 0

# Pipes
pipes = []
def create_pipe():
    height = random.randint(100, 400)
    pipes.append(pygame.Rect(WIDTH, 0, PIPE_WIDTH, height))
    pipes.append(pygame.Rect(WIDTH, height + PIPE_GAP, PIPE_WIDTH, HEIGHT - height - PIPE_GAP))

# Game Loop
running = True
score = 0
frame_count = 0

def reset_game():
    global bird, bird_velocity, pipes, score
    bird.y = BIRD_Y
    bird_velocity = 0
    pipes.clear()
    score = 0
    create_pipe()

create_pipe()
while running:
    screen.fill(WHITE)
    
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = FLAP_STRENGTH
    
    # Bird Movement
    bird_velocity += GRAVITY
    bird.y += bird_velocity
    
    # Pipe Movement
    for pipe in pipes:
        pipe.x -= PIPE_SPEED
    
    # Pipe Generation
    if frame_count % 90 == 0:
        create_pipe()
    
    # Remove Offscreen Pipes
    pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]
    
    # Collision Detection
    for pipe in pipes:
        if bird.colliderect(pipe):
            reset_game()
    if bird.y < 0 or bird.y > HEIGHT:
        reset_game()
    
    # Scoring
    if pipes and bird.x > pipes[0].x + PIPE_WIDTH:
        score += 1
        pipes.pop(0)
        pipes.pop(0)
    
    # Draw Bird
    pygame.draw.rect(screen, BLUE, bird)
    
    # Draw Pipes
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)
    
    # Draw Score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    pygame.display.flip()
    clock.tick(30)
    frame_count += 1

pygame.quit()
