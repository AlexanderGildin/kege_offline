import pygame

pygame.init()

class TextBox:
    def __init__(self, x, y, width, height, max_length, active_color=(0, 0, 150), inactive_color=(200, 200, 200), text="", screen=None, visible=True):
        pygame.scrap.init()
        self.rect = pygame.Rect(x, y, width, height)
        self.inactive_color = inactive_color  # Цвет неактивного состояния
        self.active_color = active_color  # Цвет активного состояния
        self.text = text
        self.max_length = max_length  # Максимальная длина текста
        self.screen = screen
        self.visible = visible
        self.font = pygame.font.SysFont("Arial", 24)
        self.active = False
        self.backspace_active = False

    def draw(self, screen):
        if not self.visible:
            return
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        if self.active:
            pygame.draw.rect(screen, self.active_color, self.rect, 3)
        else:
            pygame.draw.rect(screen, self.inactive_color, self.rect, 3)
        text = self.text[-self.max_length:]
        text_surface = self.font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def input(self, event):
        if not self.visible:
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL: 
                self.paste_text()
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode



    def paste_text(self):
        try:
            pygame.scrap.init()
            if pygame.scrap.get_init():
                clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                if clipboard_text:
                    clipboard_text = clipboard_text.decode("utf-8").strip("\x00")
                    self.text += clipboard_text
        except UnicodeDecodeError:
            pass
    def save_answer(self):
        return self.text

'''
if __name__ == "__main__":
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("TextBox Example")

    text_box = TextBox(100, 100, 400, 50, 4, screen=screen, visible=True)
    running = True

    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            text_box.input(event)

        text_box.draw(screen)
        pygame.display.flip()

    pygame.quit()'''