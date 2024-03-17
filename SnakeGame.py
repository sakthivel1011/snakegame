import pygame
import random

# Initialize Pygame
pygame.init()

# Set display dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Define colors
BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SNAKE_HEAD_COLOR = (0, 200, 0)
SNAKE_FOOD_COLOR = (255, 0, 0)
GAME_OVER_COLOR = (255, 255, 255)
TEXT_COLOR = (255, 255, 255)

# Set snake and snack properties
BLOCK_SIZE = 20
snake_speed = 10

# Define game states
START = 0
PLAYING = 1
GAME_OVER = 2

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# Load game font
font = pygame.font.SysFont(None, 40)

# Function to draw snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, SNAKE_COLOR, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(screen, SNAKE_HEAD_COLOR, [snake_list[0][0], snake_list[0][1], BLOCK_SIZE, BLOCK_SIZE])

# Function to display message on the screen
def display_message(msg, color, y_displacement=0):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + y_displacement))
    screen.blit(text, text_rect)

# Function to start the game
def start_game():
    snake_list = [[SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]]
    snake_length = 1
    snake_direction = 'RIGHT'
    x_snack, y_snack = generate_snack_position(snake_list)
    game_state = PLAYING
    score = 0
    high_score = load_high_score()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != 'DOWN':
                    snake_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                    snake_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                    snake_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                    snake_direction = 'RIGHT'

        if game_state == PLAYING:
            if snake_direction == 'UP':
                snake_head = [snake_list[0][0], snake_list[0][1] - BLOCK_SIZE]
            elif snake_direction == 'DOWN':
                snake_head = [snake_list[0][0], snake_list[0][1] + BLOCK_SIZE]
            elif snake_direction == 'LEFT':
                snake_head = [snake_list[0][0] - BLOCK_SIZE, snake_list[0][1]]
            elif snake_direction == 'RIGHT':
                snake_head = [snake_list[0][0] + BLOCK_SIZE, snake_list[0][1]]

            snake_list.insert(0, snake_head)

            if snake_list[0][0] == x_snack and snake_list[0][1] == y_snack:
                x_snack, y_snack = generate_snack_position(snake_list)
                snake_length += 1
                score += 1
                if score > high_score:
                    high_score = score
            else:
                snake_list.pop()

            screen.fill(BACKGROUND_COLOR)
            pygame.draw.rect(screen, SNAKE_FOOD_COLOR, [x_snack, y_snack, BLOCK_SIZE, BLOCK_SIZE])
            draw_snake(snake_list)

            # Check if snake hits itself or wall
            if (snake_list[0][0] < 0 or snake_list[0][0] >= SCREEN_WIDTH or
                    snake_list[0][1] < 0 or snake_list[0][1] >= SCREEN_HEIGHT or
                    snake_list[0] in snake_list[1:]):
                game_state = GAME_OVER
                save_high_score(high_score)

            # Display current score and high score
            display_score(score, high_score)

            pygame.display.update()
            clock.tick(snake_speed)
        
        elif game_state == GAME_OVER:
            screen.fill(BACKGROUND_COLOR)
            display_message("Game Over! Your Score: {}".format(score), GAME_OVER_COLOR, -50)
            display_message("Press SPACE to Play Again", GAME_OVER_COLOR, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        start_game()

# Function to generate snack position
def generate_snack_position(snake_list):
    while True:
        x_snack = random.randrange(0, SCREEN_WIDTH - BLOCK_SIZE, BLOCK_SIZE)
        y_snack = random.randrange(0, SCREEN_HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
        if [x_snack, y_snack] not in snake_list:
            return x_snack, y_snack

# Function to display current score and high score
def display_score(score, high_score):
    current_score_text = font.render("Score: {}".format(score), True, TEXT_COLOR)
    high_score_text = font.render("High Score: {}".format(high_score), True, TEXT_COLOR)
    screen.blit(current_score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

# Function to save high score
def save_high_score(high_score):
    with open("high_score.txt", "w") as file:
        file.write(str(high_score))

# Function to load high score
def load_high_score():
    try:
        with open("high_score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Start the game
start_game()
