import bcrypt
import pygame

from EvaDataBase import DataBase
from TimurTextInput import TextBox
from button import Button
from taskbar import Taskbar

# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PRUSSIAN = '#003153'

DBname = 'files/database'

name = ''

database = DataBase(DBname)

quest_pos = (167, 95)
max_quest_pos = (167, 95)
min_quest_pos = (167, 95)
quest_img = None

var_info = database.variant_info()

max_time = var_info['max_time_min']

pass_hash = var_info['secrkey_hash']

variant = var_info['description']

quests_ans_schema = database.get_rows_and_cols()
ans_fields_list = {}
max_width = 800
height = 45

ans_mode = False

hide_button = Button(1880, 20, '-')
hide_button.set_padding(28, 22)
hide_button.color = PRUSSIAN

end_button = Button(1610, 20, 'Завершить экзамен досрочно')
end_button.set_padding(28, 22)
end_button.color = PRUSSIAN

time_button = Button(1480, 30, '03:45:00')
time_button.color = PRUSSIAN
name_button = Button(600, 25, '')
name_button.color = PRUSSIAN
kim_button = Button(50, 25, 'КИМ')
kim_button.color = PRUSSIAN
var_button = Button(100, 25, variant)
var_button.color = PRUSSIAN
ans_button = Button(1760, 990, 'Сохранить')
ans_button.set_color(WHITE)
ans_button.text_color = '#000000'
ans_button.set_padding(40, 28)

hash_password = database.get_hashed_password()
inp_password_hash = ''
b_1 = Button(600, 360, "Введите фамилию и имя:")
e_1 = Button(1410, 400, 'enter')
e_1.set_padding(28, 28)
name_box = TextBox(600, 400, max_width, height, 30)
b_2 = Button(600, 560, "Введите пароль:")
e_2 = Button(1410, 600, 'enter')
e_2.set_padding(28, 28)
pass_box = TextBox(600, 600, max_width, height, 20)

file_names = database.get_file_names()
file_buttons = []
for quest in file_names:
    sp = []
    x_pos = 180
    for file in quest:
        button = Button(x_pos, 1000, file)
        button.rect = pygame.Rect(x_pos, 1000, 60, 60)
        sp.append(button)
        x_pos += 120
    file_buttons.append(sp)

taskbar = Taskbar(var_info['count_of_quest'], 60, 1080)

ans_list = [[] for i in range(var_info['count_of_quest'])]


# функция для рисования областей интерфейса, картинки вопроса и кнопок
def draw_ui(screen):
    screen.fill((216, 229, 242))  # Очистка экрана
    pygame.draw.rect(screen, WHITE, pygame.Rect(167, 95, 1738, 869))  # область вопроса
    screen.blit(quest_img, quest_pos)  # картинка вопроса
    pygame.draw.rect(screen, (216, 229, 242), pygame.Rect(0, 0, 1920, 95))
    pygame.draw.rect(screen, (216, 229, 242), pygame.Rect(167, 964, 1920, 95))
    pygame.draw.rect(screen, PRUSSIAN, pygame.Rect(0, 0, 1920, 80))  # фон верхней панели
    pygame.draw.rect(screen, BLACK, pygame.Rect(150, 979, 1920, 2))  # нижняя полоска
    pygame.draw.rect(screen, BLACK, pygame.Rect(150, 80, 2, 980))  # вертикальная полоска
    hide_button.draw(screen)
    end_button.draw(screen)
    taskbar.draw(screen)
    time_button.draw(screen)
    name_button.draw(screen)
    kim_button.draw(screen)
    var_button.draw(screen)
    if taskbar.current_task != 0:
        ans_button.draw(screen)
    for b in file_buttons[taskbar.current_task]:
        b.draw(screen)
        t_surface = b.font.render(b.text, True, b.text_color)
        t_rect = t_surface.get_rect()
        screen.blit(t_surface, t_rect)
    #  если не режим ответа, рисуется поле ввода/кнопка для активации режима
    if not ans_mode:
        if taskbar.current_task != 0:
            if isinstance(ans_fields_list[taskbar.current_task][0], Button):
                ans_fields_list[taskbar.current_task][0].update(pygame.mouse.get_pos())
                ans_fields_list[taskbar.current_task][0].draw(screen)
            else:
                ans_fields_list[taskbar.current_task][0].draw(screen)
    #  в режиме ответа рисуется поле ввода/сетка полей, в основном цикле в каждый из них принимается ивент
    else:
        for row in ans_fields_list[taskbar.current_task][1]:
            for field in row:
                field.draw(screen)


# обновляет текущую картинку вопроса
def update_quest_img(quest_num):
    global database, quest_img, max_quest_pos, quest_pos
    quest_img = database.quest_image(database.quest_id_by_num(quest_num))
    max_quest_pos = (167, 95 - (quest_img.get_height() - 869))
    quest_pos = (167, 95)


# функция для обновления состояний кнопок
def update_buttons():
    if ans_mode:
        ans_button.update(pygame.mouse.get_pos())
    if not ans_mode:
        end_button.update(pygame.mouse.get_pos())
        ans_button.is_hovered = False
    hide_button.update(pygame.mouse.get_pos())


pygame.init()

# Screen
WIDTH, HEIGHT = 0, 0
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

# словарь {номер вопроса: (поле, когда ввод ответа неактивен; матрица полей, когда ввод ответа активен)}
for q_num, row_col in quests_ans_schema.items():
    if row_col[0] == row_col[1] == 1:
        ans_fields_list[q_num] = ((TextBox(884, 990, max_width, height, 20),
                                   [[TextBox(884, 990, max_width, height, 20)]]))
    else:
        indent_x = 800 // row_col[1]
        input_list = [[TextBox(884 + (indent_x * j), 990 - (height * i), max_width // row_col[1], height, 20)
                       for j in range(row_col[1])] for i in range(row_col[0])]
        ans_fields_list[q_num] = (Button(1560, 990, 'Ввести ответ'), input_list)
        ans_fields_list[q_num][0].set_padding(30, 28)
        ans_fields_list[q_num][0].set_color(WHITE)
        ans_fields_list[q_num][0].set_text_color(BLACK)

if __name__ == '__main__':

    name_button.set_text(name)

    update_quest_img(taskbar.current_task)

    on_screen_running = True
    no_pass_running = True
    pass_checked = False
    if hash_password:
        while on_screen_running:
            screen.fill((216, 229, 242))
            hide_button.update(pygame.mouse.get_pos())
            e_1.update(pygame.mouse.get_pos())
            e_2.update(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on_screen_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hide_button.is_hovered:
                        pygame.display.iconify()
                    if e_1.is_hovered:
                        name = name_box.save_answer()
                        kim_button.set_text(name)
                    if e_2.is_hovered:
                        inp_password_hash = pass_box.save_answer()
                        if bcrypt.checkpw(inp_password_hash.encode("UTF-8"), hash_password):
                            pass_checked = True
                            on_screen_running = False
                name_box.input(event)
                pass_box.input(event)
            hide_button.draw(screen)
            b_1.draw(screen)
            b_2.draw(screen)
            e_1.draw(screen)
            e_2.draw(screen)
            name_box.draw(screen)
            pass_box.draw(screen)
            pygame.display.flip()

    else:
        pass_checked = True
        while no_pass_running:
            screen.fill((216, 229, 242))
            hide_button.update(pygame.mouse.get_pos())
            e_1.update(pygame.mouse.get_pos())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on_screen_running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if hide_button.is_hovered:
                        pygame.display.iconify()
                    if e_1.is_hovered:
                        name = name_box.save_answer()
                        kim_button.set_text(name)
                        no_pass_running = False
                name_box.input(event)
                pass_box.input(event)
            hide_button.draw(screen)
            b_1.draw(screen)
            e_1.draw(screen)
            name_box.draw(screen)
            pygame.display.flip()
    running = True
    if pass_checked:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # обработка действий, которые могут быть совершены вне зависимости от режима ввода ответа
                    if event.button == 1:
                        if hide_button.is_hovered:
                            pygame.display.iconify()
                            #  скроллинг
                    if event.button == 4:
                        if quest_pos[1] < min_quest_pos[1] - 30:
                            quest_pos = (167, quest_pos[1] + 30)
                    elif event.button == 5:
                        if quest_pos[1] > max_quest_pos[1] + 30:
                            quest_pos = (167, quest_pos[1] - 30)
                    # действия, которые могут быть совершены с неактивным режимом ввода ответа
                    if not ans_mode:
                        if event.button == 1:
                            taskbar.handle_event(event, pygame.mouse.get_pos())
                            update_quest_img(taskbar.current_task)
                            #  проверка на нажатие на поле активации режима ответа
                            if taskbar.current_task != 0:
                                if isinstance(ans_fields_list[taskbar.current_task][0], Button):
                                    if ans_fields_list[taskbar.current_task][0].is_hovered:
                                        ans_mode = True
                                else:
                                    ans_fields_list[taskbar.current_task][0].input(event)
                                    if ans_fields_list[taskbar.current_task][0].active:
                                        ans_fields_list[taskbar.current_task][0].active = False
                                        ans_fields_list[taskbar.current_task][1][0][0].active = True
                                        ans_mode = True

                    # режим ввода ответа
                    if ans_mode:
                        #  если нажата кнопка сохранить - выход из режима ответа, деактивация полей ввода, сохранение ответа
                        if event.button == 1:
                            if ans_button.is_hovered:
                                quest_ans = []
                                for row in ans_fields_list[taskbar.current_task][1]:
                                    for field in row:
                                        field.active = False
                                        quest_ans.append(field.save_answer())
                                ans_mode = False
                                ans_list[taskbar.current_task - 1] = quest_ans
                                print(ans_list)
                                if isinstance(ans_fields_list[taskbar.current_task][0], TextBox):
                                    ans_fields_list[taskbar.current_task][0].text = (
                                        ans_fields_list)[taskbar.current_task][1][0][0].text
                        if isinstance(ans_fields_list[taskbar.current_task][0], Button):
                            for row in ans_fields_list[taskbar.current_task][1]:
                                for field in row:
                                    field.input(event)
                #  обработка ввода текста для каждого поля, если режим ответа
                if event.type == pygame.KEYDOWN and ans_mode:
                    if event.key == pygame.K_ESCAPE:
                        for row in ans_fields_list[taskbar.current_task][1]:
                            for field in row:
                                field.active = False
                        ans_mode = False
                    for row in ans_fields_list[taskbar.current_task][1]:
                        for field in row:
                            field.input(event)
            update_buttons()
            draw_ui(screen)
            pygame.display.flip()
    pygame.quit()
    database.close()
