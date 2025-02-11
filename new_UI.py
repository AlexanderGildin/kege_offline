import pygame
from button import Button
from taskbar import Taskbar
from TimurTextInput import TextBox
from EvaDataBase import DataBase
from bcrypt import checkpw
import time
import datetime
import os


# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PRUSSIAN = '#003153'

DBname = 'files/database'

name = 'Иванов Иван'

database = DataBase(DBname)

quest_pos = (167, 95)
max_quest_pos = (167, 95)
min_quest_pos = (167, 95)
quest_img = None

var_info = database.variant_info()

if len(str(var_info['max_time_min'])) > 0:
    max_time = int(var_info['max_time_min']) * 60
# else:
#     max_time = 60000

pass_hash = var_info['secrkey_hash']

variant = var_info['description']

internet_access = bool(var_info['internet_acsess'])

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
name_button = Button(600, 25, name)
name_button.color = PRUSSIAN
kim_button = Button(50, 25, 'КИМ')
kim_button.color = PRUSSIAN
var_button = Button(100, 25, variant)
if len(variant) > 57:
    var_button.set_text(variant[:57])
var_button.color = PRUSSIAN
ans_button = Button(1760, 990, 'Сохранить')
ans_button.set_color(WHITE)
ans_button.text_color = '#000000'
ans_button.set_padding(40, 28)


taskbar = Taskbar(var_info['count_of_quest'], 60, 1080)

ans_list = [[] for i in range(var_info['count_of_quest'])]

back_btn = Button(750, 100, 'Вернуться')
back_btn.set_padding(30, 28)
back_btn.set_color((216, 229, 242))
back_btn.set_text_color(BLACK)

text_btn = Button(600, 300, f'Введите пароль для завершения варианта {variant}')
text_btn.set_color(WHITE)
text_btn.set_text_color(BLACK)

err_btn = Button(750, 700, '')
err_btn.set_color(WHITE)
err_btn.set_text_color(BLACK)

end_test_btn = Button(750, 900, 'Сохранить и выйти')
end_test_btn.set_padding(30, 28)
end_test_btn.set_color((216, 229, 242))
end_test_btn.set_text_color(BLACK)


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
    kim_button.draw(screen)
    var_button.draw(screen)
    name_button.draw(screen)
    if taskbar.current_task != 0:
        ans_button.draw(screen)

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


def save_answers(answers: list, filename):
    with open(filename, 'w') as file:
        lines = []
        file.write(f'{variant}\n{datetime.date.today().isoformat()}\n')
        for i, line in enumerate(answers):
            if len(line) == 0:
                lines.append(f"{i + 1}. _")
            else:
                lines.append(f"{i + 1}. {';'.join(line)}")
        file.write('\n'.join(lines))
        print('ответы сохранены')


def variant_func():
    global ans_fields_list, quest_pos, ans_mode, ans_button, ans_list, max_time, screen, taskbar, time_button, timing

    running = True

    is_internet = False

    while running:
        if len(str(var_info['max_time_min'])) > 0:
            #  проверка на конец времени
            if time.time() - timing > max_time:
                running = False

        if not internet_access:
            #  проверка на доступ к сети
            if int(os.system('ping google.com')) == 0:
                is_internet = True
                running = False

        #  отображение счетчика времени
        mins, secs = divmod(int(max_time - int(time.time() - timing)), 60)
        hours = mins // 60
        if len(str(var_info['max_time_min'])) > 0:
            time_button.set_text(f'{hours}:{mins % 60}:{secs}')
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
                        if end_button.is_hovered:
                            running = False
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
                                print(row)
                                for field in row:
                                    print(field, field.text)
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
            if event.type == pygame.KEYDOWN:

                if ans_mode:
                    if event.key == pygame.K_ESCAPE:
                        for row in ans_fields_list[taskbar.current_task][1]:
                            for field in row:
                                field.active = False
                        ans_mode = False
                    for row in ans_fields_list[taskbar.current_task][1]:
                        for field in row:
                            field.input(event)
        #  скроллинг по кнопкам
        if pygame.key.get_pressed()[pygame.K_UP]:
            if quest_pos[1] < min_quest_pos[1] - 30:
                quest_pos = (167, quest_pos[1] + 30)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            if quest_pos[1] > max_quest_pos[1] + 30:
                quest_pos = (167, quest_pos[1] - 30)
        update_buttons()
        draw_ui(screen)
        pygame.display.flip()

    return is_internet


def end_func():
    global screen, max_time, timing
    running = True
    message = ''
    err_btn.set_text('')

    while running:
        if len(str(var_info['max_time_min'])) > 0:
            if time.time() - timing > max_time:
                back_btn.set_text('Время закончилось')
                back_btn.set_color(WHITE)
            else:
                if not internet_access:
                    if int(os.system('ping google.com')) == 0:
                        message = 'internet_exception'
                        running = False
        else:
            if not internet_access:
                if int(os.system('ping google.com')) == 0:
                    message = 'internet_exception'
                    running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    secrkey_input.input(event)
                    if end_test_btn.is_hovered:
                        if len(pass_hash) == 0:
                            save_answers(ans_list, f'{variant}_{name}.txt')
                            message = 'End'
                            running = False
                        elif checkpw(secrkey_input.text.encode(), pass_hash):
                            save_answers(ans_list, f'{variant}_{name}.txt')
                            message = 'End'
                            running = False
                        else:
                            err_btn.set_text('Неверный пароль')
                            save_answers(ans_list, f'{name}_{variant}.txt')
                            message = 'End'
                            running = False
                    if back_btn.is_hovered:
                        if time.time() - timing < max_time:
                            message = 'Back'
                            running = False
            if event.type == pygame.KEYDOWN:
                secrkey_input.input(event)
        screen.fill(WHITE)
        end_test_btn.update(pygame.mouse.get_pos())
        if len(str(var_info['max_time_min'])) > 0:
            if time.time() - timing < max_time:
                back_btn.update(pygame.mouse.get_pos())
            else:
                back_btn.is_hovered = False
        else:
            back_btn.update(pygame.mouse.get_pos())

        back_btn.draw(screen)
        end_test_btn.draw(screen)
        secrkey_input.draw(screen)
        text_btn.draw(screen)
        err_btn.draw(screen)
        pygame.display.flip()
    return message


def internet_access_f():
    global screen
    running = True

    back_btn.set_color(RED)
    back_btn.is_hovered = False
    back_btn.set_text('Замечено подключение к интернету')

    end_test_btn.set_color(RED)
    end_test_btn.set_text('Выйти')

    err_btn.set_color(RED)
    err_btn.set_text('')

    text_btn.set_color(RED)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                secrkey_input.input(event)
                if end_test_btn.is_hovered:
                    if len(pass_hash) == 0:
                        running = False
                    elif checkpw(secrkey_input.text.encode(), pass_hash):
                        running = False
                    else:
                        err_btn.set_text('Неверный пароль')
            if event.type == pygame.KEYDOWN:
                secrkey_input.input(event)
        screen.fill(RED)
        end_test_btn.update(pygame.mouse.get_pos())
        back_btn.draw(screen)
        end_test_btn.draw(screen)
        secrkey_input.draw(screen)
        err_btn.draw(screen)
        text_btn.draw(screen)
        pygame.display.flip()
    return 'End'


pygame.init()

# Screen
WIDTH, HEIGHT = 1920, 1060
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
        ans_fields_list[q_num] = ((Button(1560, 990, 'Ввести ответ'), input_list))
        ans_fields_list[q_num][0].set_padding(30, 28)
        ans_fields_list[q_num][0].set_color(WHITE)
        ans_fields_list[q_num][0].set_text_color(BLACK)

secrkey_input = TextBox(750, 500, 300, 50, 20)


if __name__ == '__main__':
    if not internet_access:
        os.system('ipconfig/release')

    name_button.set_text(name)

    update_quest_img(taskbar.current_task)

    state = ''

    if len(str(var_info['max_time_min'])) > 0:
        timing = time.time()

    while state != 'End':
        internet_exception = variant_func()
        if internet_exception:
            state = internet_access_f()
        else:
            state = end_func()
            if state == 'internet_exception':
                state = internet_access_f()
    pygame.quit()
    database.close()

    if not internet_access:
        os.system('ipconfig/renew')
    os.remove('to_show_img.png')
