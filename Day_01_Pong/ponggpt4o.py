import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (30, 136, 229)
NEON_PINK = (255, 64, 129)
NEON_GREEN = (57, 255, 20)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Modern Pong")

# Create game objects
player = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
opponent = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball speed and direction
base_ball_speed = 7
ball_speed_x = base_ball_speed * random.choice((1, -1))
ball_speed_y = base_ball_speed * random.choice((1, -1))

# Paddle speed
base_paddle_speed = 7
paddle_speed = base_paddle_speed

# Score
player_score = 0
opponent_score = 0
font = pygame.font.Font(None, 36)

# Particles
particles = []

# Speed up timer
speed_up_timer = 0
speed_multiplier = 1.0
last_speed_up_time = 0

# Menu
menu_active = True
menu_font = pygame.font.Font(None, 48)

# Power-ups
power_up_active = False
power_up_timer = 0
power_up_effect_time = 5000  # 5 seconds
power_up = pygame.Rect(0, 0, 20, 20)
power_up_type = 0  # 0: none, 1: speed boost, 2: enlarge paddle

# Pause
paused = False

# Sound effects
hit_sound = pygame.mixer.Sound("hit.mp3")
score_sound = pygame.mixer.Sound("score.mp3")
bounce_sound = pygame.mixer.Sound("bounce.mp3")
power_up_sound = pygame.mixer.Sound("power_up.mp3")
countdown_sound = pygame.mixer.Sound("countdown.mp3")

# Background music
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

# Countdown
countdown_time = 1500  # in milliseconds
countdown_start = 0
countdown_active = False
countdown_direction = ""
trajectory_points = []

def start_countdown(direction):
    global countdown_start, countdown_active, countdown_direction, ball_speed_x, ball_speed_y
    countdown_start = pygame.time.get_ticks()
    countdown_active = True
    countdown_direction = direction
    countdown_sound.play()

    # Set initial ball speed for the countdown
    ball_speed_x = base_ball_speed * speed_multiplier * (-1 if direction == "player" else 1)
    
    # Determine the vertical direction based on the ball's position relative to the center
    if ball.centery < HEIGHT // 2:
        ball_speed_y = base_ball_speed * speed_multiplier
    elif ball.centery > HEIGHT // 2:
        ball_speed_y = -base_ball_speed * speed_multiplier
    else:
        ball_speed_y = base_ball_speed * speed_multiplier * random.choice((1, -1))

    calculate_trajectory()  # Calculate trajectory points

def calculate_trajectory():
    global trajectory_points
    trajectory_points = []
    temp_ball_x = WIDTH // 2
    temp_ball_y = HEIGHT // 2
    temp_speed_x = ball_speed_x
    temp_speed_y = ball_speed_y
    for _ in range(50):  # Calculate trajectory points for 50 frames
        temp_ball_x += temp_speed_x
        temp_ball_y += temp_speed_y
        if temp_ball_y <= 0 or temp_ball_y >= HEIGHT:
            temp_speed_y *= -1
        trajectory_points.append((temp_ball_x, temp_ball_y))

def ball_restart(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = base_ball_speed * speed_multiplier * (-1 if direction == "player" else 1)
    
    # Determine the vertical direction based on the ball's position relative to the center
    if ball.centery < HEIGHT // 2:
        ball_speed_y = base_ball_speed * speed_multiplier
    elif ball.centery > HEIGHT // 2:
        ball_speed_y = -base_ball_speed * speed_multiplier
    else:
        ball_speed_y = base_ball_speed * speed_multiplier * random.choice((1, -1))

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.life = 30
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.vx = speed * math.cos(angle)
        self.vy = speed * math.sin(angle)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        alpha = int(255 * (self.life / 30))
        color = (*self.color, alpha)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.size)

def create_particles(x, y, color, count = 20):
    for _ in range(count):
        particles.append(Particle(x, y, color))

def move_paddle(paddle, up, down):
    if up and paddle.top > 0:
        paddle.y -= paddle_speed
    if down and paddle.bottom < HEIGHT:
        paddle.y += paddle_speed

def move_opponent_ai(opponent, ball):
    if opponent.centery < ball.centery and opponent.bottom < HEIGHT:
        opponent.y += paddle_speed * 0.85  # Slightly slower than player for fairness
    elif opponent.centery > ball.centery and opponent.top > 0:
        opponent.y -= paddle_speed * 0.85

def move_ball(ball):
    global ball_speed_x, ball_speed_y, player_score, opponent_score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        create_particles(ball.centerx, ball.centery, NEON_GREEN)
        bounce_sound.play()

    if ball.left <= 0:
        opponent_score += 1
        create_particles(ball.left, ball.centery, NEON_BLUE, 50)
        score_sound.play()
        start_countdown("player")
    elif ball.right >= WIDTH:
        player_score += 1
        create_particles(ball.right, ball.centery, NEON_PINK, 50)
        score_sound.play()
        start_countdown("opponent")

    if ball.colliderect(player):
        ball_speed_x = abs(ball_speed_x)
        create_particles(ball.left, ball.centery, NEON_BLUE)
        hit_sound.play()
    elif ball.colliderect(opponent):
        ball_speed_x = -abs(ball_speed_x)
        create_particles(ball.right, ball.centery, NEON_PINK)
        hit_sound.play()

def ball_restart(direction):
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x = -base_ball_speed * speed_multiplier if direction == "player" else base_ball_speed * speed_multiplier
    ball_speed_y = base_ball_speed * speed_multiplier * random.choice((1, -1))
    print(f"Ball restart with speed: ({ball_speed_x}, {ball_speed_y})")  # Debug statement

def draw_neon_rect(surface, color, rect, width = 2):
    pygame.draw.rect(surface, color, rect)
    for i in range(3):
        pygame.draw.rect(surface, color, rect.inflate(i * 2, i * 2), 1)

def speed_up_game():
    global speed_multiplier, ball_speed_x, ball_speed_y, paddle_speed, last_speed_up_time
    if speed_multiplier < 2.0:
        speed_multiplier += 0.1
        ball_speed_x *= 1.1
        ball_speed_y *= 1.1
        paddle_speed = base_paddle_speed * speed_multiplier
        last_speed_up_time = pygame.time.get_ticks()
        create_speed_up_effect()

def create_speed_up_effect():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        particles.append(Particle(x, y, NEON_GREEN))

def draw_speed_indicator(surface):
    indicator_width = 100
    indicator_height = 10
    x = WIDTH - indicator_width - 10
    y = 10
    fill_width = int(indicator_width * (speed_multiplier - 1))
    pygame.draw.rect(surface, WHITE, (x, y, indicator_width, indicator_height), 1)
    pygame.draw.rect(surface, NEON_GREEN, (x, y, fill_width, indicator_height))

def draw_menu(surface):
    title = menu_font.render("PONG", True, WHITE)
    start_text = font.render("Press SPACE to Start", True, WHITE)
    surface.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    surface.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

def spawn_power_up():
    global power_up_active, power_up, power_up_type
    power_up_active = True
    power_up.x = random.randint(100, WIDTH - 100)
    power_up.y = random.randint(100, HEIGHT - 100)
    power_up_type = random.choice([1, 2])

def apply_power_up(player):
    global paddle_speed, speed_multiplier, power_up_active, power_up_timer
    if power_up_type == 1:  # Speed boost
        speed_multiplier += 0.5
        paddle_speed = base_paddle_speed * speed_multiplier
    elif power_up_type == 2:  # Enlarge paddle
        player.height *= 1.5
    power_up_active = False
    power_up_timer = pygame.time.get_ticks()
    power_up_sound.play()

def check_power_up_collision(player):
    if power_up_active and player.colliderect(power_up):
        apply_power_up(player)

def simulate_game():
    global ball_speed_x, ball_speed_y
    # Move ball
    ball.x += ball_speed_x * 0.5
    ball.y += ball_speed_y * 0.5

    # Bounce off top and bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1

    # Bounce off paddles
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1

    # Move AI paddles
    move_opponent_ai(player, ball)
    move_opponent_ai(opponent, ball)

    # Reset ball if it goes off-screen
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_restart()

def toggle_pause():
    global paused
    paused = not paused

def draw_pause_indicator(surface):
    pause_text = font.render("PAUSED", True, WHITE)
    surface.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - pause_text.get_height() // 2))

def draw_end_screen(surface, winner):
    end_text = menu_font.render(f"{winner} Wins!", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    surface.blit(end_text, (WIDTH // 2 - end_text.get_width() // 2, HEIGHT // 3))
    surface.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))

# Game loop
clock = pygame.time.Clock()

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if menu_active:
                    menu_active = False
                else:
                    toggle_pause()
            if event.key == pygame.K_r:
                player_score = 0
                opponent_score = 0
                menu_active = True
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()
    move_paddle(player, keys[pygame.K_w] or keys[pygame.K_UP], keys[pygame.K_s] or keys[pygame.K_DOWN])

    if menu_active:
        screen.fill(BLACK)
        simulate_game()

        # Draw blurred background game
        s = pygame.Surface((WIDTH, HEIGHT))
        s.set_alpha(100)
        s.fill(BLACK)
        
        draw_neon_rect(screen, NEON_BLUE, player)
        draw_neon_rect(screen, NEON_PINK, opponent)
        draw_neon_rect(screen, WHITE, ball)
        
        screen.blit(s, (0, 0))
        draw_menu(screen)
    else:
        if not paused:
            move_opponent_ai(opponent, ball)
            if not countdown_active:
                move_ball(ball)

            # Speed up game every 10 seconds
            if current_time - last_speed_up_time > 10000:
                speed_up_game()

            # Update particles
            particles = [p for p in particles if p.life > 0]
            for p in particles:
                p.update()

            # Power-ups
            if not power_up_active and random.randint(0, 500) == 1:
                spawn_power_up()

            if power_up_active:
                pygame.draw.rect(screen, NEON_GREEN, power_up)
                check_power_up_collision(player)

            if current_time - power_up_timer > power_up_effect_time and power_up_timer > 0:
                paddle_speed = base_paddle_speed
                player.height = PADDLE_HEIGHT
                power_up_timer = 0

            # Drawing
            screen.fill(BLACK)
            
            # Draw neon center line
            for y in range(0, HEIGHT, 20):
                pygame.draw.rect(screen, NEON_BLUE, (WIDTH // 2 - 1, y, 2, 10))

            # Draw neon paddles and ball
            draw_neon_rect(screen, NEON_BLUE, player)
            draw_neon_rect(screen, NEON_PINK, opponent)
            draw_neon_rect(screen, WHITE, ball)

            # Draw particles
            for p in particles:
                p.draw(screen)

            # Score display
            player_text = font.render(str(player_score), True, NEON_BLUE)
            opponent_text = font.render(str(opponent_score), True, NEON_PINK)
            screen.blit(player_text, (WIDTH // 4, 20))
            screen.blit(opponent_text, (3 * WIDTH // 4, 20))

            # Draw speed indicator
            draw_speed_indicator(screen)

            # Countdown
            if countdown_active:
                draw_countdown(screen)
        else:
            draw_pause_indicator(screen)

    if player_score >= 10:
        draw_end_screen(screen, "Player")
    elif opponent_score >= 10:
        draw_end_screen(screen, "Opponent")

    pygame.display.flip()
    clock.tick(FPS)
