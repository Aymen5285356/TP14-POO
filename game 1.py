import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de tir")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_width = 60
player_height = 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 7

bullets = []
bullet_speed = 10

enemies = []
enemy_width = 50
enemy_height = 30
enemy_speed = 4

score = 0
font = pygame.font.SysFont(None, 36)

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, 1000)

running = True
game_over = False
clock = pygame.time.Clock()

while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == SPAWN_ENEMY and not game_over:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append([enemy_x, 0])

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x + player_width // 2, player_y])

            if event.key == pygame.K_r and game_over:

                enemies.clear()
                bullets.clear()
                score = 0
                game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy[1] += enemy_speed

            if enemy[1] > HEIGHT:
                game_over = True

        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_width and
                    enemy[1] < bullet[1] < enemy[1] + enemy_height):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 1
                    break

    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    for bullet in bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 10))

    for enemy in enemies:
        pygame.draw.rect(screen, WHITE, (enemy[0], enemy[1], enemy_width, enemy_height))

    score_text = font.render(f"Score : {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    if game_over:
        over_text = font.render("GAME OVER - Appuyez sur R", True, RED)
        screen.blit(over_text, (80, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()