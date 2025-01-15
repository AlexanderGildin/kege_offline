import pygame

class Button:
    def __init__(self, x_pos, y_pos, text):
        # Инициализация кнопки с заданной позицией и текстом
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.pad_x = 20  # Отступ по ширине кнопки
        self.pad_y = 15  # Отступ по высоте кнопки
        self.text = text
        self.color = "#2E3E4D"  # Цвет кнопки по умолчанию
        self.default_color = '#3741b0'
        self.pressed_color = "#001e47"  # Цвет кнопки при нажатии
        self.hover_color = "#005ABB"  # Цвет кнопки при наведении
        self.text_color = "#CCCCCC"  # Цвет текста по умолчанию
        self.font = pygame.font.Font('arial.ttf', 16)  # Шрифт и размер шрифта по умолчанию
        self.is_hovered = False  # Флаг для отслеживания наведения на кнопку
        self.is_clicked = False  # Флаг для отслеживания нажатия на кнопку
        self.image = None  # Изображение на кнопке
        self.update_dimensions()  # Обновление размеров кнопки
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width + self.pad_x, self.height + self.pad_y)

    def draw(self, window):
        # Отрисовка кнопки на переданном окне
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(window, current_color, self.rect)

        if self.image:
            # Если есть изображение, отрисовываем его
            window.blit(self.image, self.rect.topleft)
        else:
            # Если изображения нет, отрисовываем текст
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            window.blit(text_surface, text_rect)

    def update_dimensions(self):
        # Обновление размеров кнопки на основе текста и размера шрифта
        text_surface = self.font.render(self.text, True, self.text_color)
        self.width, self.height = text_surface.get_size()

    def set_padding(self, pad_x, pad_y):
        # Установка отступов для ширины и высоты кнопки и обновление размеров
        self.pad_x, self.pad_y = pad_x, pad_y
        self.update_dimensions()
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width + self.pad_x, self.height + self.pad_y)

    def set_pos(self, x_pos, y_pos):
        # Установка позиции кнопки и обновление прямоугольника
        self.x_pos, self.y_pos = x_pos, y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width + self.pad_x, self.height + self.pad_y)

    def set_text(self, text):
        # Установка текста кнопки и обновление размеров и прямоугольника
        self.text = text
        self.update_dimensions()
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width + self.pad_x, self.height + self.pad_y)

    def set_color(self, color):
        # Установка цвета кнопки
        self.color = color

    def set_default_color(self):
        self.color = self.default_color

    def set_clicked_color(self):
        self.color = self.pressed_color

    def set_hover_color(self, hover_color):
        # Установка цвета кнопки при наведении
        self.hover_color = hover_color

    def set_text_color(self, text_color):
        # Установка цвета текста
        self.text_color = text_color

    def click_toggle(self):
        # переключатель состояния нажатия на кнопку
        if self.is_clicked:
            self.is_clicked = False
        else:
            self.is_clicked = True

    def update(self, mouse_pos):
        # Обновление состояния наведения на основе позиции мыши
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def set_image(self, image_path):
        # Установка изображения на кнопку и его масштабирование под размер кнопки
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))