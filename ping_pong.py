import pygame
import random
import sys




pygame.init()


WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пинг-Понг: Игрок против Бота")

def draw_text_and_buttons(winner=None, clicked_button=None):

    player_text = font.render(str(player_score), True, WHITE)
    bot_text = font.render(str(bot_score), True, RED)
    screen.blit(player_text, (WIDTH - 200, 20))
    screen.blit(bot_text, (50, 20))


    if winner:
        result_text = font.render(winner, True, WHITE)
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 3))


        exam_button = pygame.Rect(WIDTH // 3 - 150, HEIGHT // 2, 300, 60)
        pygame.draw.rect(screen, WHITE, exam_button)
        screen.blit(font_small.render("Пройти ЕГЭ", True, BLACK), (exam_button.x + 50, exam_button.y + 10))

        round_button = pygame.Rect(2 * WIDTH // 3 - 150, HEIGHT // 2, 300, 60)
        pygame.draw.rect(screen, WHITE, round_button)
        screen.blit(font_small.render("Новый Раунд", True, BLACK), (round_button.x + 30, round_button.y + 10))

        return exam_button, round_button

    return None, None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)


pygame.mixer.init()
try:
    pygame.mixer.music.load("muc.mp3")
    pygame.mixer.music.play(-1)
    music_on = True
except:
    music_on = False


FPS = 60
clock = pygame.time.Clock()


PADDLE_WIDTH, PADDLE_HEIGHT = 20, 150
BALL_SIZE = 20


font = pygame.font.Font(None, 74)
font_small = pygame.font.Font(None, 50)


player_score = 0
bot_score = 0


stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]


class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def move(self, up, down):
        keys = pygame.key.get_pressed()
        if keys[up] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[down] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-8, 8])
        self.speed_y = random.choice([-8, 8])

    def update(self):
        global player_score, bot_score
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

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


def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    music_on = not music_on

def new_round():
    global player_score, bot_score, game_over
    player_score = 0
    bot_score = 0
    game_over = False
    ball.reset()

def take_exam():
    pass

player = Paddle(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2)
bot = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
ball = Ball()

all_sprites = pygame.sprite.Group()
all_sprites.add(player, bot, ball)


settings_button = pygame.Rect(WIDTH - 100, 20, 60, 60)


show_settings = False


show_rules = True


rules_image = pygame.image.load("rules.png")
rules_image = pygame.transform.scale(rules_image, (WIDTH, HEIGHT))


exam_button = pygame.Rect(WIDTH // 3 - 150, HEIGHT - 200, 300, 80)
play_button = pygame.Rect(2 * WIDTH // 3 - 150, HEIGHT - 200, 300, 80)


running = True
game_over = False
clicked_button = None
winner=None

music_button = pygame.Rect(0, 0, 300, 60)
restart_button = pygame.Rect(0, 0, 300, 60)
exam_start_button = pygame.Rect(0, 0, 300, 60)
while running:
    screen.fill(BLACK)

    if show_rules:  # Если включен экран правил
        screen.blit(rules_image, (0, 0))

        pygame.draw.rect(screen, WHITE, exam_button)
        pygame.draw.rect(screen, WHITE, play_button)

        screen.blit(font_small.render("Пройти ЕГЭ", True, BLACK),
                    (exam_button.x + 50, exam_button.y + 20))
        screen.blit(font_small.render("Играть в пинг-понг", True, BLACK),
                    (play_button.x + 30, play_button.y + 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exam_button.collidepoint(event.pos):
                    take_exam()  # Вызывает "Пройти ЕГЭ"
                elif play_button.collidepoint(event.pos):
                    show_rules = False  # Запускаем пинг-понг

        continue



    for i in range(len(stars)):
        x, y = stars[i]
        pygame.draw.circle(screen, YELLOW, (x, y), 2)
        stars[i] = (x, y + 1 if y + 1 < HEIGHT else 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and show_settings:
            if music_button.collidepoint(event.pos):
                toggle_music()


        if event.type == pygame.MOUSEBUTTONDOWN:
            if settings_button.collidepoint(event.pos):
                show_settings = not show_settings

        if event.type == pygame.MOUSEBUTTONDOWN and show_settings:
            if restart_button.collidepoint(event.pos):
                new_round()
                show_settings = False

        if event.type == pygame.MOUSEBUTTONDOWN and show_settings:
            if restart_button.collidepoint(event.pos):
                new_round()
                show_settings = False

        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            mouse_pos = pygame.mouse.get_pos()
            exam_button, round_button = draw_text_and_buttons(winner, clicked_button)

            if exam_button and exam_button.collidepoint(mouse_pos):
                clicked_button = "exam"
            elif round_button and round_button.collidepoint(mouse_pos):
                clicked_button = "round"

    if event.type == pygame.MOUSEBUTTONUP and game_over:
        mouse_pos = pygame.mouse.get_pos()


        if clicked_button == "exam" and exam_button.collidepoint(mouse_pos):
            take_exam()
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

    if not game_over and not show_settings:
        player.move(pygame.K_UP, pygame.K_DOWN)

        if bot.rect.centery < ball.rect.centery and bot.rect.bottom < HEIGHT:
            bot.rect.y += bot.speed
        if bot.rect.centery > ball.rect.centery and bot.rect.top > 0:
            bot.rect.y -= bot.speed

        ball.update()

        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(bot.rect):
            ball.speed_x *= -1

    all_sprites.draw(screen)
    draw_text_and_buttons()
    if game_over:
        draw_text_and_buttons(winner, clicked_button)

    pygame.draw.circle(screen, BLUE, settings_button.center, 30)
    pygame.draw.circle(screen, WHITE, settings_button.center, 25, 5)  # Внешний контур


    if show_settings:
        pygame.draw.rect(screen, GRAY, (WIDTH // 3, HEIGHT // 3, WIDTH // 3, HEIGHT // 3))

        music_button.topleft = (WIDTH // 3 + 50, HEIGHT // 3 + 50)
        restart_button.topleft = (WIDTH // 3 + 50, HEIGHT // 3 + 150)
        exam_start_button.topleft = (WIDTH // 3 + 50, HEIGHT // 3 + 250)

        pygame.draw.rect(screen, WHITE, music_button)
        pygame.draw.rect(screen, WHITE, restart_button)
        pygame.draw.rect(screen, WHITE, exam_start_button)

        screen.blit(font_small.render("Музыка: " + ("Вкл" if music_on else "Выкл"), True, BLACK),
                    (music_button.x + 20, music_button.y + 10))
        screen.blit(font_small.render("Новый матч", True, BLACK), (restart_button.x + 40, restart_button.y + 10))
        screen.blit(font_small.render("Начать ЕГЭ", True, BLACK), (exam_start_button.x + 40, exam_start_button.y + 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()