import pygame

from button import Button


class Taskbar:
    def __init__(self, num_tasks, width, height):
        self.num_tasks = num_tasks
        self.current_task = 1
        self.scroll_offset = 0
        self.tasks_per_page = 10
        self.info_button_pressed = False
        self.answers_count = 0
        self.width = width
        self.height = height
        self.button_size = 55
        self.buttons = []
        self.info_button = Button(35, 130, "i")
        self.info_button.rect = pygame.Rect(self.info_button.x_pos, self.info_button.y_pos, self.button_size,
                                            self.button_size)
        self.up_button = Button(35, 200, "↑")
        self.up_button.rect = pygame.Rect(self.up_button.x_pos, self.up_button.y_pos, self.button_size,
                                          self.button_size)
        self.down_button = Button(35, 945, "↓")
        self.down_button.rect = pygame.Rect(self.down_button.x_pos, self.down_button.y_pos, self.button_size,
                                            self.button_size)
        self.create_task_buttons()

    def create_task_buttons(self):
        self.buttons.clear()
        for i in range(self.num_tasks):
            y_pos = 270 + (i - self.scroll_offset) * (self.button_size + 12)
            button = Button(35, y_pos, f"{i + 1}")
            button.set_padding(0, 0)  # Убираем отступы для квадратных кнопок
            button.update_dimensions()  # Пересчитываем размеры кнопки
            button.rect = pygame.Rect(button.x_pos, button.y_pos, self.button_size,
                                      self.button_size)  # Устанавливаем квадратный размер
            self.buttons.append(button)

    def draw(self, screen):

        # Рисуем счетчик ответов
        font = pygame.font.Font(None, 36)
        text = font.render(f"Ответы: {self.answers_count}", True, (0, 0, 0))
        screen.blit(text, (18, 92))

        # Рисуем кнопку информации
        self.info_button.draw(screen)

        # Рисуем кнопки заданий
        for button in self.buttons[self.scroll_offset:self.scroll_offset + self.tasks_per_page]:
            button.draw(screen)

        # Рисуем кнопку прокрутки вверх
        self.up_button.draw(screen)

        # Рисуем кнопку прокрутки вниз
        self.down_button.draw(screen)

    def handle_event(self, event, mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяем клик по кнопке информации
            if self.info_button.rect.collidepoint(mouse_pos):
                self.info_button_pressed = not self.info_button_pressed
                self.current_task = 0

            # Проверяем клик по кнопкам заданий
            for button in self.buttons[self.scroll_offset:self.scroll_offset + self.tasks_per_page]:
                if button.rect.collidepoint(mouse_pos):
                    self.current_task = int(button.text)
                    button.click_toggle()

            # Проверяем клик по кнопке прокрутки вверх
            if self.up_button.rect.collidepoint(mouse_pos) and self.scroll_offset > 0:
                self.scroll_offset -= 1
                self.create_task_buttons()

            # Проверяем клик по кнопке прокрутки вниз
            if self.down_button.rect.collidepoint(
                    mouse_pos) and self.scroll_offset + self.tasks_per_page < self.num_tasks:
                self.scroll_offset += 1
                self.create_task_buttons()

        # Обновляем состояние кнопок
        self.info_button.update(mouse_pos)
        for button in self.buttons[self.scroll_offset:self.scroll_offset + self.tasks_per_page]:
            button.update(mouse_pos)
        self.up_button.update(mouse_pos)
        self.down_button.update(mouse_pos)

    def check_clicked(self):
        for button in self.buttons[self.scroll_offset:self.scroll_offset + self.tasks_per_page]:
            if button.is_clicked:
                return True
            else:
                continue
        return False
    def increment_answers(self):
        self.answers_count += 1

    def decrement_answers(self):
        if self.answers_count > 0:
            self.answers_count -= 1
