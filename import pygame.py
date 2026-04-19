import pygame
import sys
import random
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lumberjack Game")

clock = pygame.time.Clock()

# Colors
DARK_BG = (30, 30, 40)
GRASS_BASE = (50, 160, 70)
GRASS_VARIATION = [(45,150,65), (55,170,75), (40,140,60)]
TREE_TRUNK = (100, 60, 30)
TREE_LEAVES = (30, 120, 40)
WHITE = (255,255,255)
HOVER = (200, 200, 255)

# Player
player_x, player_y = WIDTH//2, HEIGHT//2
speed = 4

# Axe animation
swinging = False
swing_angle = 0

# Trees
trees = []
for _ in range(25):
    trees.append((random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)))

# Fonts
title_font = pygame.font.SysFont("arial", 64, bold=True)
menu_font = pygame.font.SysFont("arial", 40)

state = "menu"

# --------- DRAW FUNCTIONS ---------

def draw_grass():
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            color = random.choice(GRASS_VARIATION)
            pygame.draw.rect(screen, color, (x, y, 20, 20))

def draw_trees():
    for (tx, ty) in trees:
        pygame.draw.rect(screen, TREE_TRUNK, (tx-5, ty, 10, 20))
        pygame.draw.circle(screen, TREE_LEAVES, (tx, ty), 20)

def draw_player():
    # body
    pygame.draw.circle(screen, (220, 180, 140), (player_x, player_y-10), 10)  # head
    pygame.draw.rect(screen, (50, 100, 200), (player_x-8, player_y, 16, 25))  # body

def draw_axe():
    global swing_angle

    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - player_x
    dy = mouse_y - player_y
    angle = math.atan2(dy, dx)

    if swinging:
        swing_offset = math.sin(swing_angle) * 1.5
        angle += swing_offset

    # Axe position
    length = 30
    end_x = player_x + math.cos(angle) * length
    end_y = player_y + math.sin(angle) * length

    # Handle
    pygame.draw.line(screen, (139,69,19), (player_x, player_y), (end_x, end_y), 4)

    # Blade
    blade_x = end_x + math.cos(angle) * 5
    blade_y = end_y + math.sin(angle) * 5
    pygame.draw.circle(screen, (200,200,200), (int(blade_x), int(blade_y)), 6)

def update_axe():
    global swinging, swing_angle
    if swinging:
        swing_angle += 0.3
        if swing_angle > math.pi:
            swinging = False
            swing_angle = 0

# --------- MENU ---------

def draw_menu():
    screen.fill(DARK_BG)

    title = title_font.render("LUMBERJACK", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

    mouse = pygame.mouse.get_pos()

    play_rect = pygame.Rect(WIDTH//2-100, 280, 200, 60)
    exit_rect = pygame.Rect(WIDTH//2-100, 360, 200, 60)

    # Hover effect
    pygame.draw.rect(screen, HOVER if play_rect.collidepoint(mouse) else WHITE, play_rect, 2)
    pygame.draw.rect(screen, HOVER if exit_rect.collidepoint(mouse) else WHITE, exit_rect, 2)

    play_text = menu_font.render("PLAY", True, WHITE)
    exit_text = menu_font.render("EXIT", True, WHITE)

    screen.blit(play_text, (play_rect.centerx - play_text.get_width()//2, play_rect.y+10))
    screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()//2, exit_rect.y+10))

    return play_rect, exit_rect

# --------- GAME ---------

def game():
    global player_x, player_y

    draw_grass()
    draw_trees()
    draw_player()
    draw_axe()
    update_axe()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_y -= speed
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_y += speed
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_x -= speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_x += speed

# --------- MAIN LOOP ---------

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_rect, exit_rect = draw_menu()
                if play_rect.collidepoint(event.pos):
                    state = "game"
                if exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        elif state == "game":
            if event.type == pygame.MOUSEBUTTONDOWN:
                swinging = True

    if state == "menu":
        draw_menu()

    elif state == "game":
        game()

    pygame.display.flip()