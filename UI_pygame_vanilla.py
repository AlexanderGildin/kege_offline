import pygame
from backend import InputBox
from button import Button

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

t_button_1 = Button(200, 200, ' 1 ')
t_button_1.set_padding(35,25)
t_button_2 = Button(200, 245, ' 2 ')
t_button_2.set_padding(35,25)
t_button_3 = Button(200, 290, ' 3 ')
t_button_3.set_padding(35,25)
t_button_4 = Button(200, 335, ' 4 ')
t_button_4.set_padding(35,25)
t_button_5 = Button(200, 380, ' 5 ')
t_button_5.set_padding(35,25)
t_button_6 = Button(200, 425, ' 6 ')
t_button_6.set_padding(35,25)
t_button_7 = Button(200, 470, ' 7 ')
t_button_7.set_padding(35,25)
t_button_8 = Button(200, 515, ' 8 ')
t_button_8.set_padding(35,25)
t_button_9 = Button(200, 560, ' 9 ')
t_button_9.set_padding(35,25)
t_button_10 = Button(200, 605, '10 ')
t_button_10.set_padding(35,25)
t_button_11 = Button(200, 650, '11 ')
t_button_11.set_padding(35,25)
t_button_12 = Button(200, 695, '12 ')
t_button_12.set_padding(35,25)
t_button_13 = Button(200, 740, '13 ')
t_button_13.set_padding(35,25)
t_button_14 = Button(200, 785, '14 ')
t_button_14.set_padding(35,25)
t_button_15 = Button(200, 830, '15 ')
t_button_15.set_padding(35,25)
hide_button = Button(1650, 110, '-')
hide_button.set_padding(28,22)
close_button = Button(1688, 110, 'X')
close_button.set_padding(28,22)
close_button.set_color(RED)


t_buttons = [t_button_1, t_button_2, t_button_3, t_button_4, t_button_5, t_button_6, t_button_7,
           t_button_8, t_button_9, t_button_10, t_button_11, t_button_12, t_button_13, t_button_14, t_button_15]


if __name__ == '__main__':



    running = True
    while running:
        screen.fill((255, 255, 255))  # Очистка экрана
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for button in t_buttons:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button.is_hovered:
                        for b in t_buttons:
                            b.is_clicked = False
                        button.click_toggle()
                if button.is_clicked:
                    button.set_clicked_color()
                if not button.is_clicked:
                    button.set_default_color()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if close_button.is_hovered:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hide_button.is_hovered:
                        pygame.display.iconify()
        for button in t_buttons:
            button.update(pygame.mouse.get_pos())
            button.draw(screen)

        close_button.update(pygame.mouse.get_pos())
        close_button.draw(screen)
        hide_button.update(pygame.mouse.get_pos())
        hide_button.draw(screen)
        pygame.draw.rect(screen, WHITE, pygame.Rect(250, 200, 100, 1080))
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 190, 1920, 2))
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 150, 1920, 2))
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 880, 1920, 3))
        pygame.draw.rect(screen, BLACK, pygame.Rect(260, 150, 2, 730))
        pygame.display.flip()

    pygame.quit()




