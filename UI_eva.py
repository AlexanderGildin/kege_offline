import pygame
from button import Button
from TimurTextInput import TextBox

pygame.init()

# Screen
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PRUSSIAN = '#003153'

hide_button = Button(1880, 20, '-')
hide_button.set_padding(28,22)
hide_button.color = PRUSSIAN

end_button = Button(1610, 20, 'Завершить экзамен досрочно')
end_button.set_padding(28,22)
end_button.color = PRUSSIAN

text_box = TextBox(1400, 1016, 300, 49, 20)


time_button = Button(1480, 30, '03:45:00')
time_button.color = PRUSSIAN
name_button = Button(600, 25, 'Иванов Иван')
name_button.color = PRUSSIAN
kim_button = Button(50, 25, 'КИМ')
kim_button.color = PRUSSIAN
var_button = Button(100, 25, '....')
var_button.color = PRUSSIAN
ans_button = Button(1760, 1016, 'Сохранить')
ans_button.set_color(WHITE)
ans_button.text_color = '#000000'
ans_button.set_padding(40, 32)

if __name__ == '__main__':
    running = True
    while running:
        screen.fill((216, 229, 242))  # Очистка экрана
        pygame.draw.rect(screen, PRUSSIAN, pygame.Rect(0, 0, 1920, 80)) #фон верхней панели
        pygame.draw.rect(screen, WHITE, pygame.Rect(167, 95, 1738, 889)) #область вопроса
        pygame.draw.rect(screen, BLACK, pygame.Rect(150, 999, 1920, 2)) #нижняя полоска
        pygame.draw.rect(screen, BLACK, pygame.Rect(150, 80, 2, 1000)) #вертикальная полоска
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            text_box.input(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hide_button.is_hovered:
                    pygame.display.iconify()
        hide_button.update(pygame.mouse.get_pos())
        hide_button.draw(screen)
        end_button.update(pygame.mouse.get_pos())
        end_button.draw(screen)

        text_box.draw(screen)
        time_button.draw(screen)
        name_button.draw(screen)
        kim_button.draw(screen)
        var_button.draw(screen)
        ans_button.draw(screen)

        pygame.display.flip()

    pygame.quit()
