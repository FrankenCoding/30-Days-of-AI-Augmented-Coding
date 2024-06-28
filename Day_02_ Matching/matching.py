import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stock Up Matching Game")

# Colors
DARK_BLUE = (0, 20, 80)
BLUE = (0, 70, 180)
LIGHT_BLUE = (100, 180, 255)
RED = (255, 50, 50)
WHITE = (255, 255, 255)
GREEN = (50, 200, 50)

# Load fonts
title_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 28)
card_font = pygame.font.Font(None, 24)

# Game variables
grid_size = 3
grid = [[None for _ in range(grid_size)] for _ in range(grid_size)]
symbols = ['A', 'B', 'C']  # Replace with actual symbols or images later
remaining_rounds = 5

def draw_rounded_rect(surface, color, rect, radius=10):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def draw_background():
    screen.fill(DARK_BLUE)
    # Draw city skyline
    for i in range(0, WIDTH, 30):
        height = random.randint(50, 150)
        pygame.draw.rect(screen, BLUE, (i, HEIGHT - height, 20, height))

def draw_grid():
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(250 + col * 110, 180 + row * 110, 100, 100)
            draw_rounded_rect(screen, LIGHT_BLUE, rect)
            if grid[row][col]:
                text = card_font.render(grid[row][col], True, DARK_BLUE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                text1 = card_font.render("NO CHANGES", True, DARK_BLUE)
                text2 = card_font.render("AVAILABLE", True, DARK_BLUE)
                screen.blit(text1, (rect.centerx - text1.get_width() // 2, rect.centery - 15))
                screen.blit(text2, (rect.centerx - text2.get_width() // 2, rect.centery + 15))

def draw_ui():
    # Draw title
    title = title_font.render("Stock Up", True, RED)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

    # Draw remaining rounds
    rounds_rect = pygame.Rect(WIDTH - 220, 20, 200, 40)
    draw_rounded_rect(screen, LIGHT_BLUE, rounds_rect)
    rounds_text = button_font.render(f"Remaining rounds: {remaining_rounds}", True, DARK_BLUE)
    screen.blit(rounds_text, (rounds_rect.centerx - rounds_text.get_width() // 2, rounds_rect.centery - rounds_text.get_height() // 2))

    # Draw buttons
    daily_tasks_rect = pygame.Rect(20, 20, 150, 50)
    draw_rounded_rect(screen, RED, daily_tasks_rect)
    daily_tasks = button_font.render("Daily Tasks", True, WHITE)
    screen.blit(daily_tasks, (daily_tasks_rect.centerx - daily_tasks.get_width() // 2, daily_tasks_rect.centery - daily_tasks.get_height() // 2))

    exchange_store_rect = pygame.Rect(20, 80, 150, 50)
    draw_rounded_rect(screen, GREEN, exchange_store_rect)
    exchange_store = button_font.render("Exchange Store", True, WHITE)
    screen.blit(exchange_store, (exchange_store_rect.centerx - exchange_store.get_width() // 2, exchange_store_rect.centery - exchange_store.get_height() // 2))

    pre_register_rect = pygame.Rect(WIDTH - 180, HEIGHT - 60, 160, 40)
    draw_rounded_rect(screen, GREEN, pre_register_rect)
    pre_register = button_font.render("Pre-register Now", True, WHITE)
    screen.blit(pre_register, (pre_register_rect.centerx - pre_register.get_width() // 2, pre_register_rect.centery - pre_register.get_height() // 2))

    # Draw additional buttons
    share_rect = pygame.Rect(WIDTH - 180, HEIGHT - 110, 160, 40)
    draw_rounded_rect(screen, LIGHT_BLUE, share_rect)
    share = button_font.render("Share This Event", True, DARK_BLUE)
    screen.blit(share, (share_rect.centerx - share.get_width() // 2, share_rect.centery - share.get_height() // 2))

    lucky_rect = pygame.Rect(WIDTH - 180, HEIGHT - 160, 160, 40)
    draw_rounded_rect(screen, LIGHT_BLUE, lucky_rect)
    lucky = button_font.render("Lucky Prize", True, DARK_BLUE)
    screen.blit(lucky, (lucky_rect.centerx - lucky.get_width() // 2, lucky_rect.centery - lucky.get_height() // 2))

def check_match():
    # Check rows, columns, and diagonals for matches
    for i in range(grid_size):
        if grid[i][0] == grid[i][1] == grid[i][2] != None:  # Check rows
            return True
        if grid[0][i] == grid[1][i] == grid[2][i] != None:  # Check columns
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] != None:  # Check diagonal
        return True
    if grid[0][2] == grid[1][1] == grid[2][0] != None:  # Check other diagonal
        return True
    return False

def flip_card(row, col):
    global remaining_rounds
    if grid[row][col] is None and remaining_rounds > 0:
        grid[row][col] = random.choice(symbols)
        remaining_rounds -= 1
        if check_match():
            print("Match found!")
            # Here you could add points, clear the grid, etc.

def main():
    global remaining_rounds
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = (x - 250) // 110
                row = (y - 180) // 110
                if 0 <= row < grid_size and 0 <= col < grid_size:
                    flip_card(row, col)

        draw_background()
        draw_grid()
        draw_ui()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()