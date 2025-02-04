import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг: Игрок против Бота")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
gray = (100, 100, 100)

# Частота кадров
fps = 60
clock = pygame.time.Clock()

paddle_width, paddle_h = 20, 150
ball_size = 20
font = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)


player_score = 0
bot_score = 0


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((paddle_width, paddle_h))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 6

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ball_size, ball_size))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-8, 8])
        self.speed_y = random.choice([-8, 8])

    def update(self):
        global player_score, bot_score
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отражение от верхнего и нижнего краёв
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        # Проверка выхода за границы
        if self.rect.left <= 0:
            player_score += 1
            self.reset()
        if self.rect.right >= WIDTH:
            bot_score += 1
            self.reset()

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x *= random.choice([-1, 1])
        self.speed_y *= random.choice([-1, 1])

# Создание объектов
player = Paddle(WIDTH - 40, HEIGHT // 2 - paddle_h // 2)
bot = Paddle(20, HEIGHT // 2 - paddle_h // 2)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player, bot, ball)

# Функция для кнопки "Пройти ЕГЭ"
def go_to_exam():
    pass


# Функция для нового раунда
def new_round():
    global player_score, bot_score
    player_score = 0
    bot_score = 0
    ball.reset()

def draw_all_sprites(winner=None, clicked_button=None):

    player_text = font.render(str(player_score), True, white)
    bot_text = font.render(str(bot_score), True, red)
    screen.blit(player_text, (WIDTH - 200, 20))
    screen.blit(bot_text, (50, 20))

    if winner:
        result_text = font.render(winner, True, white)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))

        exam_button = pygame.Rect(WIDTH // 3 - 150, HEIGHT // 2, 300, 60)
        round_button = pygame.Rect(2 * WIDTH // 3 - 150, HEIGHT // 2, 300, 60)

        exam_color = white if clicked_button != "exam" else black
        round_color = white if clicked_button != "round" else black

        pygame.draw.rect(screen, exam_color, exam_button)
        exam_text = font_small.render("Пройти ЕГЭ", True, black if clicked_button != "exam" else white)
        screen.blit(exam_text, (exam_button.x + 50, exam_button.y + 10))

        pygame.draw.rect(screen, round_color, round_button)
        round_text = font_small.render("Новый Раунд", True, black if clicked_button != "round" else white)
        screen.blit(round_text, (round_button.x + 30, round_button.y + 10))

        return exam_button, round_button

    return None, None


running = True
game_over = False
clicked_button = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            exam_button, round_button = draw_all_sprites(winner, clicked_button)

            if exam_button and exam_button.collidepoint(mouse_pos):
                clicked_button = "exam"
            elif round_button and round_button.collidepoint(mouse_pos):
                clicked_button = "round"

        if event.type == pygame.MOUSEBUTTONUP and game_over:
            mouse_pos = pygame.mouse.get_pos()
            exam_button, round_button = draw_all_sprites(winner, clicked_button)

            if clicked_button == "exam" and exam_button.collidepoint(mouse_pos):
                go_to_exam()
            elif clicked_button == "round" and round_button.collidepoint(mouse_pos):
                new_round()
                game_over = False


            clicked_button = None


    if player_score >= 3:
        game_over = True
        winner = "Вы выиграли!"
    elif bot_score >= 3:
        game_over = True
        winner = "Вы проиграли!"

    if not game_over:
        player.move(pygame.K_UP, pygame.K_DOWN)

        if bot.rect.centery < ball.rect.centery and bot.rect.bottom < HEIGHT:
            bot.rect.y += bot.speed
        if bot.rect.centery > ball.rect.centery and bot.rect.top > 0:
            bot.rect.y -= bot.speed
        ball.update()

        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(bot.rect):
            ball.speed_x *= -1

    screen.fill(black)
    all_sprites.draw(screen)

    if game_over:
        draw_all_sprites(winner, clicked_button)
    else:
        draw_all_sprites()

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()