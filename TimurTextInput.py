import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Текстовое поле")

class TextBox:
    def __init__(self, x, y, width, height, max_length, active_color=(0, 0, 150), inactive_color=(200, 200, 200), text="", color_frame=(0, 0, 255), screen=None, visible = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color # цвет кнопки
        self.active_color = active_color #цвет обводки при вводе текста
        self.text = text
        self.max_length = max_length #максимальный размер текста     
        self.screen = screen
        self.visible = visible
        self.font = pygame.font.Font(None, 24) 

        self.active = False 
        if visible:
            self.draw(screen)

    def draw(self, screen):
        pygame.draw.rect(screen, self.inactive_color, self.rect)
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect, 3)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect, 3) 
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def input(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if not self.active:
                return
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                if self.text:
                    self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                return self.text
            elif len(self.text) < self.max_length:
                self.text += event.unicode
        self.draw(self.screen)



text_box = TextBox(200, 200, 400, 50, 20, screen=screen, visible=True)
running = True
screen.fill((0, 0, 0))
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        text_box.input(event)
    
    pygame.display.flip()


pygame.quit()
