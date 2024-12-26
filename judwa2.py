import pygame
import sys
import random

# Initialize Pygame and mixer for sound
pygame.init()
pygame.mixer.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mirror World: Dynamic Edition")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Background setup
background = pygame.image.load("background.jpeg")  # Add your background image here
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
bg_y = 0  # Vertical position of the background

# Player properties
PLAYER_SIZE = 40
player1_pos = [WIDTH // 4, HEIGHT // 2]
player2_pos = [3 * WIDTH // 4, HEIGHT // 2]
player_speed = 5
speed_increment = 0.1

# Obstacles
obstacles = [
    pygame.Rect(WIDTH // 3, HEIGHT // 3, 50, 50),
    pygame.Rect(2 * WIDTH // 3, 2 * HEIGHT // 3, 50, 50)
]

# Goal zones
goal1 = pygame.Rect(WIDTH // 4, HEIGHT // 4, PLAYER_SIZE * 2, PLAYER_SIZE * 2)
goal2 = pygame.Rect(3 * WIDTH // 4, 3 * HEIGHT // 4, PLAYER_SIZE * 2, PLAYER_SIZE * 2)

# Danger zones
danger_zones = [
    pygame.Rect(WIDTH // 4, 3 * HEIGHT // 4, 100, 50),
    pygame.Rect(3 * WIDTH // 4, HEIGHT // 4, 100, 50)
]

# Timer and score
level_time = 300  # Increased timer for easier gameplay
start_ticks = pygame.time.get_ticks()
score = 0
score_limit = 10

# Sound effects
bg_music = pygame.mixer.Sound("bg_music.mp3")  # Add background music file
win_sound = pygame.mixer.Sound("win_sound.mp3")  # Add win sound file
lose_sound = pygame.mixer.Sound("lose_sound.mp3")  # Add lose sound file
bg_music.play(-1)  # Loop background music

# Weather effects
snowflakes = [{"x": random.randint(0, WIDTH), "y": random.randint(-HEIGHT, 0)} for _ in range(30)]

# Random position function for goals and obstacles
def randomize_positions():
    global goal1, goal2, obstacles
    goal1.x = random.randint(0, WIDTH - PLAYER_SIZE * 2)
    goal1.y = random.randint(0, HEIGHT - PLAYER_SIZE * 2)
    
    goal2.x = random.randint(0, WIDTH - PLAYER_SIZE * 2)
    goal2.y = random.randint(0, HEIGHT - PLAYER_SIZE * 2)

    obstacles = [
        pygame.Rect(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, 50),
        pygame.Rect(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, 50)
    ]

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:  # Player 1 up
        player1_pos[1] -= player_speed
        player2_pos[1] += player_speed
    if keys[pygame.K_s]:  # Player 1 down
        player1_pos[1] += player_speed
        player2_pos[1] -= player_speed
    if keys[pygame.K_a]:  # Player 1 left
        player1_pos[0] -= player_speed
        player2_pos[0] += player_speed
    if keys[pygame.K_d]:  # Player 1 right
        player1_pos[0] += player_speed
        player2_pos[0] -= player_speed

    # Check for collisions with obstacles
    player1_rect = pygame.Rect(player1_pos[0], player1_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    player2_rect = pygame.Rect(player2_pos[0], player2_pos[1], PLAYER_SIZE, PLAYER_SIZE)

    for obstacle in obstacles:
        if player1_rect.colliderect(obstacle) or player2_rect.colliderect(obstacle):
            print("Game Over! You hit an obstacle.")
            lose_sound.play()
            running = False

    # Check if either player reaches their goal
    if player1_rect.colliderect(goal1) or player2_rect.colliderect(goal2):
        score += 1
        print(f"Score: {score}")
        if score >= score_limit:
            print("You Win! Score limit reached.")
            win_sound.play()
            running = False
        else:
            player1_pos = [WIDTH // 4, HEIGHT // 2]
            player2_pos = [3 * WIDTH // 4, HEIGHT // 2]
            player_speed += speed_increment
            randomize_positions()  # Change positions of goals and obstacles after each score
            # Add a new barrier (increase difficulty)
            obstacles.append(pygame.Rect(random.randint(0, WIDTH - 50), random.randint(0, HEIGHT - 50), 50, 50))

    # Check if either player hits a danger zone
    for danger_zone in danger_zones:
        if player1_rect.colliderect(danger_zone) or player2_rect.colliderect(danger_zone):
            print("Game Over! You hit a danger zone.")
            lose_sound.play()
            running = False

    # Check timer
    elapsed_time = (pygame.time.get_ticks() - start_ticks) // 1000
    if elapsed_time >= level_time:
        print("Time's up! Game Over.")
        lose_sound.play()
        running = False

    # Draw everything
    screen.fill(WHITE)

    # Scroll background
    bg_y += 1
    if bg_y >= HEIGHT:
        bg_y = 0
    screen.blit(background, (0, bg_y))
    screen.blit(background, (0, bg_y - HEIGHT))

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, obstacle)

    # Draw goal zones
    pygame.draw.rect(screen, GREEN, goal1)
    pygame.draw.rect(screen, GREEN, goal2)

    # Draw danger zones
    for danger_zone in danger_zones:
        pygame.draw.rect(screen, RED, danger_zone)

    # Draw snowflakes (weather effect)
    for flake in snowflakes:
        flake["y"] += 1
        if flake["y"] > HEIGHT:
            flake["y"] = random.randint(-20, -1)
            flake["x"] = random.randint(0, WIDTH)
        pygame.draw.circle(screen, WHITE, (flake["x"], flake["y"]), 3)

    # Draw players
    pygame.draw.rect(screen, BLUE, player1_rect)
    pygame.draw.rect(screen, BLACK, player2_rect)

    # Draw timer and score
    timer_text = pygame.font.Font(None, 36).render(f"Time: {level_time - elapsed_time}", True, BLACK)
    score_text = pygame.font.Font(None, 36).render(f"Score: {score}/{score_limit}", True, BLACK)
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
