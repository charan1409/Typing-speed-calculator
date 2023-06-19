import pygame
import sys
import random
import time

pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Fonts
FONT_SIZE = 30
FONT = pygame.font.Font(None, FONT_SIZE)

# Game settings
BALL_RADIUS = 50
FALL_SPEED = 1
GAME_DURATION = 30
WORDS = []
# Open the file for reading
with open('words.txt', 'r') as file:
    # Read each line from the file and add it to the array
    for line in file:
        WORDS.append(line.strip())


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Game")
clock = pygame.time.Clock()


class Ball:
    def __init__(self):
        self.word = random.choice(WORDS)
        self.x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
        self.y = -BALL_RADIUS
        self.radius = BALL_RADIUS
        self.color = RED
        self.speed = FALL_SPEED

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        text = FONT.render(self.word, True, WHITE)
        screen.blit(text, (self.x - text.get_width() //
                    2, self.y - text.get_height() // 2))

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = (dx * dx + dy * dy) ** 0.5
        if distance <= self.radius + other.radius:
            if self.y < other.y:
                # Return self as the ball to remove
                return self
            else:
                # Return other as the ball to remove
                return other
        return None

pop_sound = pygame.mixer.Sound("pop.mp3")
BALLS_PER_POP = 1
ball_count = 0

balls = []
balls_popped = 0
ball_count = 0
start_time = time.time()
current_word = ""

# Difficulty levels
easy_text = FONT.render("Easy", True, WHITE)
easy_rect = easy_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2))
screen.blit(easy_text, easy_rect)

medium_text = FONT.render("Medium", True, WHITE) 
medium_rect = medium_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(medium_text, medium_rect)

hard_text = FONT.render("Hard", True, WHITE)
hard_rect = hard_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2))
screen.blit(hard_text, hard_rect)

# Display quit button
quit_text = FONT.render("Quit", True, WHITE)
quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
screen.blit(quit_text, quit_rect)
game_started = False  # Game has not started yet
pygame.display.flip()

BALLS_PER_POP = 2
ball_frequency = 1.0
difficulty = None

while True:
    # Process events
    for event in pygame.event.get():
        # Check if user clicked start or quit button
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if easy_rect.collidepoint(event.pos):
                difficulty = "easy"
                # Start game
                FALL_SPEED = 1
                start_time = time.time()
                current_word = ""
                ball_count = 0
                balls_popped = 0
                balls = []
                game_started = True
            elif medium_rect.collidepoint(event.pos):
                difficulty = "medium"
                # Start game
                FALL_SPEED = 1.5
                start_time = time.time()
                current_word = ""
                ball_count = 0
                balls_popped = 0
                balls = []
                game_started = True
            elif hard_rect.collidepoint(event.pos):
                difficulty = "hard"
                # Start game
                FALL_SPEED = 1.75
                start_time = time.time()
                current_word = ""
                ball_count = 0
                balls_popped = 0
                balls = []
                game_started = True
            elif quit_rect.collidepoint(event.pos):
                # Quit game
                pygame.quit()
                sys.exit()
        elif event.type == pygame.KEYDOWN:
            if game_started:
                if event.key == pygame.K_SPACE:
                    for ball in balls:
                        if ball.word == current_word:  # If match, pop ball
                            balls.remove(ball)
                            balls.append(Ball())
                            if balls_popped>2:
                                balls.append(Ball())
                            pop_sound.play() # Play pop sound
                            balls_popped += 1
                            current_word = ""
                            break
                elif event.key == pygame.K_BACKSPACE:
                    current_word = current_word[:-1]
                else:
                    current_word += event.unicode

    if game_started:
        screen.fill(BLACK)
        if int(time.time() - start_time) < GAME_DURATION:
            if ball_count == 0:
                balls.append(Ball())
                ball_count += 1
            elif len(balls) < ball_count * BALLS_PER_POP:
                # Generate new balls based on ball_frequency
                if time.time() - GAME_DURATION >= ball_frequency:
                    for i in range(BALLS_PER_POP):
                        balls.append(Ball())
                    # GAME_DURATION = time.time()
                    last_ball_time = time.time()

            balls_to_remove = []
            for i in range(len(balls)):
                for j in range(i + 1, len(balls)):
                    ball_to_remove = balls[i].check_collision(balls[j])
                    if ball_to_remove:
                        balls_to_remove.append(ball_to_remove)
            for ball in balls_to_remove:
                if ball in balls:
                    balls.remove(ball)

            for ball in balls:
                ball.update()
                ball.draw()

            timer_text = FONT.render(
                f"Time: {GAME_DURATION - int(time.time() - start_time)}", True, RED)
            screen.blit(timer_text, (10, 10))

            current_word_text = FONT.render(current_word, True, WHITE)
            screen.blit(current_word_text, (10, HEIGHT -
                        current_word_text.get_height() - 10))

            balls_popped_text = FONT.render(
                f"Balls Popped: {balls_popped}", True, WHITE)
            screen.blit(balls_popped_text, (WIDTH - balls_popped_text.get_width() -
                        10, HEIGHT - balls_popped_text.get_height() - 10))


            # Check if time is up
            if time.time() - start_time >= GAME_DURATION:
                # Display game over message
                game_over_text = FONT.render(
                    f"Game Over! Your typing speed: {(balls_popped/30)*60} !", True, WHITE)
                game_over_rect = game_over_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(game_over_text, game_over_rect)

                game_over_text2 = FONT.render(
                    f"Your score: {balls_popped}", True, WHITE)
                game_over_rect2 = game_over_text2.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + 50))
                screen.blit(game_over_text2, game_over_rect2)

                # Display play again and quit buttons
                play_again_text = FONT.render("Play Again", True, WHITE)
                play_again_rect = play_again_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + 100))
                screen.blit(play_again_text, play_again_rect)

                pygame.display.flip()

                # Wait for user input
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if play_again_rect.collidepoint(event.pos):
                                # Start game again
                                start_time = time.time()
                                current_word = ""
                                ball_count = 0
                                balls_popped = 0
                                balls = []
                                break
                            elif quit_rect.collidepoint(event.pos):
                                # Quit game
                                pygame.quit()
                                sys.exit()
                    else:
                        continue
                    break

        else:
            # Display game over message
            game_over_text = FONT.render(
                f"Game Over! Your typing speed: {(balls_popped/30)*60} !", True, WHITE)
            game_over_rect = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, game_over_rect)

            game_over_text2 = FONT.render(
                f"Your score: {balls_popped}", True, WHITE)
            game_over_rect2 = game_over_text2.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50))
            screen.blit(game_over_text2, game_over_rect2)

            # Display play again and quit buttons
            play_again_text = FONT.render("Play Again", True, WHITE)
            play_again_rect = play_again_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 100))
            screen.blit(play_again_text, play_again_rect)

            pygame.display.flip()

            # Wait for user input
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if play_again_rect.collidepoint(event.pos):
                            # Start game again
                            start_time = time.time()
                            current_word = ""
                            ball_count = 0
                            balls_popped = 0
                            balls = []
                            break
                        elif quit_rect.collidepoint(event.pos):
                            # Quit game
                            pygame.quit()
                            sys.exit()
                else:
                    continue
                break

        pygame.display.flip()
        clock.tick(60)
