from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from PyQt6.QtCore import QThread, pyqtSignal
from QtRedactorUI import Ui_MainWindow
from EvaDataBaseCreate import DataBase
from bcrypt import hashpw, gensalt
from uniteImages import image_size_changes
import os
import time
import shutil

# https://habr.com/ru/companies/simbirsoft/articles/701020/

class insertVariant(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str)

    def __init__(self, text):
        QThread.__init__(self)
        self.text = text

    def run(self):
        debug = False
        files = []
        # text - список из строк окна описания варианта. Он передан в класс при создании его экземпляра
        secrkey_hash = ''
        max_time_min = ''  # там предполагается int
        internet_acsess = 0

        #  получение параметров варианта
        for i in range(8):
            if self.text[i].startswith('COUNT_OF_QUESTIONS'):
                count_of_quest = int(self.text[i].split('=')[1])
            if self.text[i].startswith('MAXTIME'):
                if len(self.text[1].split('=')[1]) > 0 and self.text[1].split('=')[1] != '0':
                    max_time_min = int(self.text[1].split('=')[1])
            if self.text[i].startswith('KEY'):
                if len(self.text[2].split('=')[1]) > 0:
                    secrkey_hash = hashpw(bytes(self.text[2].split('=')[1], 'utf-8'), salt=gensalt())
            if self.text[i].startswith('DESCRIPTION'):
                description = self.text[i].split('=')[1]
            if self.text[i].startswith('INTERNET_ACCESS'):
                if self.text[i].split('=')[1] == '1':
                    internet_acsess = 1
        database = DataBase(description + '.db')
        DB_with_ans = DataBase(f"{description}_ans.db")
        database.create_tables()
        DB_with_ans.create_tables()
        database.clear_tables()
        DB_with_ans.clear_tables()

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
        if debug: print(self.text)
        try:
            for i in range(4, len(self.text)):
                if debug: print("очередная строка ", i)
                #  если начался новый вопрос/информация, записываются в бд и сбрасываются в переменной собранные данные
                if self.text[i].startswith('I ') or self.text[i].startswith('Q'):
                    if debug: print("отработка строки 75", self.text[i], i)
                    if len(quest_data) > 0:
                        if quest_data[0][1] != "Info":
                            database.new_quest(quest_data)
                            DB_with_ans.new_quest(ans_data)
                        else:
                            database.new_quest(quest_data)
                    if self.text[i].startswith('I '):
                        quest_data = [("number", "Info")]
                    else:
                        quest_data = [("number", int(self.text[i].split()[0][1:]))]
                        ans_data = [("number", int(self.text[i].split()[0][1:]))]
                    required_width = int(self.text[i].split(' ')[1])
                    self.progress_signal.emit((self.text[i].split()[0][1:]))
                    if debug: print((self.text[i].split()[0][1:]))
                    # if debug: time.sleep(10)
                    continue
                param = self.text[i].split('=')
                #  обработка возможных полей и добавление их значений в quest_data
                if param[0] == 'IMG':
                    lname = param[1].replace(' ', '')
                    lname = lname.replace(';', ',')
                    image_size_changes(lname.split(','), required_width, result_file_name='../questImg.png')
                    with open('../questImg.png', 'rb') as image:
                        quest_bytes = image.read()
                    quest_data.append(("question", quest_bytes))

                elif param[0] == 'FILES':
                    lifn = param[1].replace(" ", '')
                    lifn = lifn.replace(',', ';')
                    quest_data.append(("files", lifn))
                    file_split = lifn.split(';')
                    for x in file_split:
                        if len(x) > 0:
                            files.append(x)
                elif param[0] == 'SANS':
                    quest_data.append(("rows_in_answ", param[1].split(', ')[0]))
                    quest_data.append(("col_in_answ", param[1].split(', ')[1]))
                    ans_data.append(("rows_in_answ", param[1].split(', ')[0]))
                    ans_data.append(("col_in_answ", param[1].split(', ')[1]))
                elif param[0] == 'POINTS':
                    ans_data.append(('points', param[1])) #добавляем в базу ответов
                elif param[0] == 'SEP':
                    ans_data.append(("info", f"separator='{param[1]}'"))
                elif param[0] == 'ANSW':
                    ans_data.append(("answer", param[1]))
                if debug: print("отработка строки 121")
            #  запись последнего невошедшего вопроса
            database.new_quest(quest_data)
            DB_with_ans.new_quest(ans_data)
        except Exception as ex:
            if debug: print("сработала ошибка в строке 127", str(ex))
            self.progress_signal.emit(str(ex))
            pass

        database.close()
        files.append(f'{description}.db')
        for x in files:
            shutil.copy(x, str(os.getcwd() + r'\files' + "\\" + x))  # ЗАМЕНИТЬ НА MOVE
        shutil.make_archive(f'{description}', 'zip', root_dir='../files')  # Похоже, что создает даже если такой был уже
        try:
            os.rename(f'{description}.zip', f'{description}.tsk')
        except:
            os.remove(f'{description}.tsk')
            os.rename(f'{description}.zip', f'{description}.tsk')

        self.finished_signal.emit(description)

        shutil.rmtree('../files')


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("QT Редактор вариантов")

        self.question_number_q = 1
        self.insert_into_db.clicked.connect(self.funct_check_file)
        self.add_quest.clicked.connect(self.add_question_funct)
        try:
            os.makedirs(os.getcwd() + r'\files')
        except FileExistsError:
            shutil.rmtree('../files')
            os.makedirs(os.getcwd() + r'\files')



    def funct_check_file(self):
        flag_img = False
        flag_img_i = False
        q_num_list = []
        flag_count_of_question = True
        flag_description = True
        self.count_of_question = ' '
        self.q_num = '1'
        answer_list = []
        error_output = []
        number_of_questions = 1
        text = self.dataTextEdit.toPlainText().split('\n')

        try:
            for i in range(4):
                if flag_count_of_question:
                    if 'COUNT_OF_QUESTIONS' not in text[i]:
                        flag_count_of_question = True
                if text[i].startswith('COUNT_OF_QUESTIONS'):
                    self.count_of_question = int(text[i].split('=')[1])
                    flag_count_of_question = False

                if flag_description:
                    if 'DESCRIPTION' not in text[i]:
                        flag_description = True
                if text[i].startswith('DESCRIPTION'):
                    flag_description = False

            if flag_count_of_question:
                error_output.append('Ошибка: отсутствует строка: COUNT_OF_QUESTIONS=')
            if flag_description:
                error_output.append('Ошибка: отсутствует строка: DESCRIPTION=')
            for i in range(len(text)):
                #  если начался новый вопрос/информация, записываются в бд и сбрасываются в переменной собранные данные
                if text[i].startswith('I '):
                    if text[i].startswith('I '):
                        self.quest_data = [("number", "Info")]
                    else:
                        self.quest_data = [("number", int(text[i].split()[0][1:]))]
                    self.required_width = int(text[i].split(' ')[1])
                    continue
                self.param = text[i].split('=')
                if len(self.param) > 1:
                    self.param[1] = ''.join(self.param[1].split())
                #  обработка возможных полей и добавление их значений в quest_data
                if self.param[0].startswith('Q'):
                    self.q_num = self.param[0].split()[0][1:]
                    self.question_number_q = self.q_num
                    q_num_list.append(self.q_num)
                # if self.param[0] == 'IMG_I':
                #     try:
                #         if len(self.param[1].split()) != 0:
                #             flag_img_i = True
                #             for x in self.param[1].split(';'):
                #                 self.sep_img_i = ';'
                #                 if os.path.exists(os.path.dirname(__file__)+"\\"+x) == False:
                #                     for y in self.param[1].split(','):
                #                         self.sep_img_i = ','
                #                         if os.path.exists(os.path.dirname(__file__)+"\\"+y) == False:
                #                             flag_img_i = False
                #         if len(self.param[1]) != 0 or self.param[0].startswith('Q') and flag_img_i:
                #             image_size_changes(self.param[1].split(self.sep_img_i), self.required_width,
                #                                result_file_name='questImg.png')
                #         else:
                #             error_output.append(
                #                 str("Ошибка" + f": Указанные файлы изображений {text[i]} не найдены"))
                #     except FileNotFoundError:
                #         error_output.append(
                #             str("Ошибка" + f": Указанные файлы изображений {text[i]} не найдены"))
                if self.param[0] == 'IMG':
                    try:
                        if len(self.param[1].split()) != 0:
                            flag_img = True
                            for x in self.param[1].split(';'):
                                self.sep_img = ';'
                                if os.path.exists(os.getcwd() + "\\" + x) == False:
                                    for y in self.param[1].split(','):
                                        self.sep_img = ','
                                        if os.path.exists(os.getcwd() + "\\" + y) == False:
                                            flag_img = False
                        # if len(self.param[1]) != 0 or self.param[0].startswith('Q') and flag_img:
                        #     image_size_changes(self.param[1].split(self.sep_img), self.required_width,
                        #                        result_file_name='questImg.png')
                        if len(self.param[1]) == 0 or not flag_img:
                            error_output.append(str("Ошибка" + f": Вопрос {str(self.q_num)} Указанные файлы изображений {text[i]} не найдены {os.getcwd()} type 1"))
                    except FileNotFoundError:
                        if self.param[0].startswith('Q'):
                            error_output.append(
                                str("Ошибка (в Q" + str(
                                    self.q_num) + f"): Указанные файлы изображений {text[i]} не найдены {os.getcwd()} type 2"))
                        else:
                            error_output.append(str("Ошибка" + f": Указанные файлы изображений {text[i]} не найдены {os.getcwd()} type 3"))
                if self.param[0] == 'SANS':
                    number_of_questions_list = self.param[1].split(',')
                    number_of_questions = int(number_of_questions_list[0]) * int(number_of_questions_list[1])
                if self.param[0] == 'SEP':
                    self.param[1] = ''.join(self.param[1].split())
                    separator = self.param[1]
                if self.param[0] == 'FILES':
                    try:
                        if len(self.param[1].split()) != 0:
                            for x in self.param[1].split(';'):
                                self.sep_files = ';'
                                if os.path.exists(os.getcwd() + "\\" + x) == False:
                                    for y in self.param[1].split(','):
                                        self.sep_files = ','
                                        if os.path.exists(os.getcwd() + "\\" + y) == False:
                                            error_output.append(str('Ошибка (в Q' +
                                                                    str(self.q_num)
                                                                    + f'): Указанные файлы изображений {text[i]} не найдены {os.getcwd()} type 4'))
                    except FileNotFoundError:
                        error_output.append(str('Ошибка (в Q' +
                                                str(self.q_num)
                                                + f'): Указанные файлы изображений {text[i]} не найдены {os.getcwd()} type 5'))
                if self.param[0] == 'ANSW':
                    if (len(self.param[1].split(separator)) != number_of_questions or self.param[1] == ''
                            and number_of_questions != 0):
                        error_output.append(str('Ошибка (в Q' +
                                                str(self.q_num)
                                                + '): Не соответствует количество ответов ANSW='))
                        #  raise NoResponse
                    else:
                        answer_list.append(self.param[1].split(separator))
            self.logsTextEdit.setPlainText('Дождитесь окончания формирования варианта.')
        except Exception:
            error_output.append('Неизвестная ошибка в вопросе Q' + str(self.q_num))
        if int(self.q_num) != int(self.count_of_question):
            error_output.append('Ошибка: не совпадает количество вопросов')
        for x in q_num_list:
            if int(x) > self.count_of_question or len(set(q_num_list)) != len(q_num_list):
                error_output.append('Ошибка: неправильная нумерация вопросов')
                break
        if len(error_output) > 0:
            self.logsTextEdit.setPlainText('\n'.join(error_output))
        if len(error_output) == 0:
            self.myinsertObject = insertVariant(self.dataTextEdit.toPlainText().split('\n'))
            self.myinsertObject.progress_signal.connect(self.updatelog)
            self.myinsertObject.finished_signal.connect(self.unblock)
            self.insert_into_db.setEnabled(False)
            self.dataTextEdit.setEnabled(False)
            self.add_quest.setEnabled(False)
            self.myinsertObject.start()

    def updatelog(self, x):
        self.logsTextEdit.setPlainText(f"Обработка вопроса: {x}")

    def unblock(self, file_name):
        self.logsTextEdit.setPlainText(
            f'Создан файл КИМ: {file_name}.tsk, поместите его в станцию тестирования.\nСоздан файл: '
            f'{file_name}_ans.db, поместите его в станцию проверки.')
        self.insert_into_db.setEnabled(True)
        self.dataTextEdit.setEnabled(True)
        self.add_quest.setEnabled(True)

    def add_question_funct(self):
        self.question_number_q = int(self.question_number_q) + 1
        self.dataTextEdit.setPlainText(
            self.dataTextEdit.toPlainText() + "\nQ" + str(self.question_number_q) + " 1730\n"
                                                                                    "IMG=p" + str(
                self.question_number_q) + '.png\n'
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
