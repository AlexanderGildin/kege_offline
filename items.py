from button import Button
from taskbar import Taskbar
from TimurTextInput import TextBox
from EvaDataBase import DataBase


# Standard RGB colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 100, 100)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PRUSSIAN = '#003153'

DBname = 'files/database.db'

name = 'Иванов Иван'

variant = '....'

database = DataBase(DBname)

quest_pos = (167, 95)
max_quest_pos = (167, 95)
min_quest_pos = (167, 95)
quest_img = None

var_info = database.variant_info()

max_time = var_info['max_time_min']

pass_hash = var_info['secrkey_hash']

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
var_button.color = PRUSSIAN
ans_button = Button(1760, 990, 'Сохранить')
ans_button.set_color(WHITE)
ans_button.text_color = '#000000'
ans_button.set_padding(40, 28)


taskbar = Taskbar(var_info['count_of_quest'], 60, 1080)

ans_list = [[] for i in range(var_info['count_of_quest'])]
