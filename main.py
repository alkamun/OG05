import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 600, 800
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apples Invaders")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Игрок
rocket_img = pygame.image.load("img/rocket.png")
rocket_img.set_colorkey(WHITE)
player_width, player_height = 72, 71
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 7

# Пуля
bullet_width, bullet_height = 4, 15
bullet_speed = 10
bullets = []

# Враги
bug_img = pygame.image.load("img/apple.png")
enemy_width, enemy_height = 48, 58
bug_img = pygame.transform.scale(bug_img, (enemy_width, enemy_height))

enemy_rows = 5
enemy_cols = 8
enemy_gap = 20
enemy_speed = 2
enemy_direction = 1  # 1 - вправо, -1 - влево
enemies = []

# Очки
round_cnt = 1
score = 0
font = pygame.font.SysFont("Arial", 28)

# Загрузка врагов
def create_enemies():
    enemies.clear()
    for row in range(enemy_rows):
        for col in range(enemy_cols):
            x = col * (enemy_width + enemy_gap) + 50
            y = row * (enemy_height + enemy_gap) + 50
            enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

create_enemies()

clock = pygame.time.Clock()

def draw_window():
    win.fill(WHITE)

    # Игрок
    win.blit(rocket_img, (player_x, player_y))

    # Пули
    for bullet in bullets:
        pygame.draw.rect(win, (255, 0, 0), bullet)

    # Враги
    for enemy in enemies:
        win.blit(bug_img, enemy)

    # Очки
    score_text = font.render(f"Score: {score} Round: {round_cnt}", True, BLACK)
    win.blit(score_text, (10, 10))

    pygame.display.update()

def draw_round():
    gameover_text = font.render(f"Round {round_cnt}", True, BLACK)
    win.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

win.fill(WHITE)
draw_round()
pygame.time.wait(1000)

# Основной цикл игры
running = True
while running:
    clock.tick(60)

    # События
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        if not bullets or bullets[-1].y < player_y - 60:  # Ограничение на частоту выстрелов
            bullet = pygame.Rect(player_x + player_width // 2 - bullet_width // 2,
                                 player_y, bullet_width, bullet_height)
            bullets.append(bullet)

    # Движение пуль
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)
        else:
            # Проверка столкновения с врагом
            for enemy in enemies:
                if bullet.colliderect(enemy):
                    try:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                    except ValueError:
                        pass
                    break

    # Движение врагов
    move_down = False
    for enemy in enemies:
        enemy.x += enemy_speed * enemy_direction
        if enemy.x <= 0 or enemy.x >= WIDTH - enemy_width:
            move_down = True
    if move_down:
        enemy_direction *= -1
        for enemy in enemies:
            enemy.y += enemy_height // 2

    # Проверка проигрыша
    for enemy in enemies:
        if enemy.y + enemy_height >= player_y:
            running = False

    draw_window()

    # Победа (если все враги уничтожены)
    if not enemies:
        round_cnt += 1
        draw_round()
        pygame.time.wait(1000)
        create_enemies()

# Конец игры
win.fill(WHITE)
gameover_text = font.render("Game Over", True, BLACK)
win.blit(gameover_text, (WIDTH//2 - gameover_text.get_width()//2, HEIGHT//2))
pygame.display.update()
pygame.time.wait(1000)
pygame.quit()
sys.exit()