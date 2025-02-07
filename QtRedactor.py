from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from QtRedactorUI import Ui_MainWindow
from EvaDataBase import DataBase
from bcrypt import hashpw, gensalt
from uniteImages import image_size_changes
import os
import shutil


class NoResponse(Exception):
    pass


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("QT Редактор вариантов")

        #  self.insert_into_db.clicked.connect(self.insertVariant)
        self.question_number_q = 1
        self.insert_into_db.clicked.connect(self.funct_check_file)
        self.add_quest.clicked.connect(self.add_question_funct)
        try:
            os.makedirs(os.getcwd() + r'\files')
        except FileExistsError:
            shutil.rmtree('files')
            os.makedirs(os.getcwd() + r'\files')

    def insertVariant(self):
        files = []
        text = self.dataTextEdit.toPlainText().split('\n')
        description = text[3].split('=')[1]
        #  открытие бд и получение строк текста редактора
        database = DataBase(description)
        DB_with_ans = DataBase(f"{description}_ans")
        database.create_tables()
        database.clear_tables()  # очистка таблиц если вариант создается повторно
        DB_with_ans.create_tables()
        DB_with_ans.clear_tables()

        #  получение параметров варианта
        count_of_quest = int(text[0].split('=')[1])
        if len(text[1].split('=')[1]) > 0 and text[1].split('=')[1] != '0':
            max_time_min = int(text[1].split('=')[1])
        internet_acsess = 0
        if len(text[2].split('=')[1]) > 0:
            secrkey_hash = hashpw(bytes(text[2].split('=')[1], 'utf-8'), salt=gensalt())

        #  запись варианта
        database.update_variants(
            description=description,
            count_of_quest=count_of_quest,
            max_time_min=max_time_min,
            internet_acsess=internet_acsess,
            secrkey_hash=secrkey_hash
        )

        #  последовательная запись вопросов:

        # quest_data - переменная со значениями текущего вопроса/информации
        quest_data = []
        ans_data = []

        #  необходимая конечная ширина изображения вопроса
        required_width = 1730

        #  количество строк по варианту фиксировано, поэтому начинаю сразу со строк по вопросам
        i = 4
        try:
            for i in range(4, len(text)):
                #  если начался новый вопрос/информация, записываются в бд и сбрасываются в переменной собранные данные
                if text[i].startswith('I ') or text[i].startswith('Q'):
                    if len(quest_data) > 0:
                        if quest_data[0][1] != "Info":
                            database.new_quest(quest_data)
                            DB_with_ans.new_quest(ans_data)
                        else:
                            database.new_quest(quest_data)
                    if text[i].startswith('I '):
                        quest_data = [("number", "Info")]
                    else:
                        quest_data = [("number", int(text[i].split()[0][1:]))]
                        ans_data = [("number", int(text[i].split()[0][1:]))]
                    required_width = int(text[i].split(' ')[1])
                    continue
                param = text[i].split('=')

                #  обработка возможных полей и добавление их значений в quest_data
                if param[0] == 'IMG':
                    image_size_changes(param[1].split(', '), required_width, result_file_name='questImg.png')
                    with open('questImg.png', 'rb') as image:
                        quest_bytes = image.read()
                    quest_data.append(("question", quest_bytes))

                elif param[0] == 'FILES':
                    quest_data.append(("files", param[1]))
                    files.append(param[1])
                elif param[0] == 'SANS':
                    quest_data.append(("rows_in_answ", param[1].split(', ')[0]))
                    quest_data.append(("col_in_answ", param[1].split(', ')[1]))
                    ans_data.append(("rows_in_answ", param[1].split(', ')[0]))
                    ans_data.append(("col_in_answ", param[1].split(', ')[1]))
                elif param[0] == 'SEP':
                    quest_data.append(("info", f"separator='{param[1]}'"))
                elif param[0] == 'ANSW':
                    ans_data.append(("answer", param[1]))
            #  запись последнего невошедшего вопроса
            database.new_quest(quest_data)
            DB_with_ans.new_quest(ans_data)
            self.logsTextEdit.setPlainText('Лог:')
        except:
            pass

        database.close()
        for x in files:
            shutil.copy(x, str(os.getcwd() + r'\files'))
        try:
            os.makedirs(os.getcwd() + r'\to_archive')
        except FileExistsError:
            shutil.rmtree('to_archive')
            os.makedirs(os.getcwd() + r'\to_archive')
        shutil.copy('files', 'to_archive')
        shutil.copy('variant_27.db', 'to_archive')
        shutil.make_archive('archive', 'zip', root_dir='to_archive')

    def funct_check_file(self):
        q_num = '1'
        answer_list = []
        error_output = []
        number_of_questions = 1
        text = self.dataTextEdit.toPlainText().split('\n')
        try:
            for i in range(4):
                if text[i].startswith('COUNT_OF_QUESTIONS'):
                    self.count_of_question = int(text[0].split('=')[1])
            for i in range(4, len(text)):
                #  если начался новый вопрос/информация, записываются в бд и сбрасываются в переменной собранные данные
                if text[i].startswith('I '):
                    if text[i].startswith('I '):
                        self.quest_data = [("number", "Info")]
                    else:
                        self.quest_data = [("number", int(text[i].split()[0][1:]))]
                    self.required_width = int(text[i].split(' ')[1])
                    continue
                self.param = text[i].split('=')

                #  обработка возможных полей и добавление их значений в quest_data
                if self.param[0].startswith('Q'):
                    q_num = self.param[0].split()[0][1]
                if self.param[0] == 'IMG':
                    if len(self.param[1]) != 0 or self.param[0].startswith('Q'):
                        image_size_changes(self.param[1].split(', '), self.required_width,
                                           result_file_name='questImg.png')
                    else:
                        error_output.append(
                            str("Ошибка (в Q" + str(
                                q_num) + f"): Указанные файлы изображений ({text[i]}) не найдены"))
                        #  raise FileNotFoundError
                if self.param[0] == 'FILES':
                    if len(self.param[1]) == 0:
                        error_output.append(
                            str("Ошибка (в Q" + str(
                                q_num) + f"): Указанные файлы изображений ({text[i]}) не найдены"))
                        #  raise FileNotFoundError
                if self.param[0] == 'SANS':
                    number_of_questions_list = self.param[1].split(', ')
                    number_of_questions = int(number_of_questions_list[0]) * int(number_of_questions_list[1])
                if self.param[0] == 'SEP':
                    self.param[1] = ''.join(self.param[1].split())
                    separator = self.param[1]
                if self.param[0] == 'ANSW':
                    if (len(self.param[1].split(separator)) != number_of_questions or self.param[1] == ''
                            and number_of_questions != 0):
                        error_output.append(str('Ошибка (в Q' +
                                                str(q_num)
                                                + '): Не соответствует количество ответов (ANSW=)'))
                        #  raise NoResponse
                    else:
                        answer_list.append(self.param[1].split(separator))
            self.logsTextEdit.setPlainText('ОК')
        except FileNotFoundError:
            pass
        except NoResponse:
            pass
        if self.question_number_q != self.count_of_question:
            error_output.append('Ошибка: не совпадает количество ответов')
        if len(error_output) > 0:
            self.logsTextEdit.setPlainText('\n'.join(error_output))
        if len(error_output) == 0:
            self.insertVariant()
            self.logsTextEdit.setPlainText('Вариант создан')

    def add_question_funct(self):
        self.question_number_q += 1
        self.dataTextEdit.setPlainText(
            self.dataTextEdit.toPlainText() + "\nQ" + str(self.question_number_q) + " 1730\n"
                                                                                    "IMG=\n"
                                                                                    "FILES=\n"
                                                                                    "SANS=1, 1\n"
                                                                                    "SEP=;\n"
                                                                                    "ANSW=")


class WindowScroller(QScrollArea):
    def __init__(self):
        super().__init__()

        self.wdg = MainWindow()

        self.setWidget(self.wdg)

        self.setGeometry(0, 0, self.wdg.width(), self.wdg.height())


if __name__ == "__main__":
    app = QApplication([])
    window = WindowScroller()
    window.show()
    app.exec()
