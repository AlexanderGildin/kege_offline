import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FONT_SIZE = 24


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Текстовое поле")

font = pygame.font.Font(None, FONT_SIZE)


class TextBox:
    def __init__(self, x, y, width, height, max_length):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = (200, 200, 200)
        self.active_color = (0, 0, 150)
        self.text = ""
        self.max_length = max_length
        self.active = False
    def draw(self, screen):
        pygame.draw.rect(screen, (100, 100, 100), self.rect)
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect, 2)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect, 2) 
        text_surface = font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif len(self.text) < self.max_length:
                self.text += event.unicode


text_box = TextBox(200, 200, 400, 50, 20)

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        text_box.input(event)

    text_box.draw(screen)

    
    pygame.display.flip()

pygame.quit()