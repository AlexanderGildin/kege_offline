from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from QtRedactorUI import Ui_MainWindow
from EvaDataBase import DataBase
from bcrypt import hashpw, gensalt
from uniteImages import image_size_changes

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("QT Редактор вариантов")

        self.insert_into_db.clicked.connect(self.insertVariant)

    def insertVariant(self):
        #  открытие бд и получение строк текста редактора
        database = DataBase()
        database.create_tables()
        database.clear_tables()  # очистка таблиц если вариант создается повторно
        text = self.dataTextEdit.toPlainText().split('\n')

        #  получение параметров варианта
        count_of_quest = int(text[0].split('=')[1])
        max_time_min = int(text[1].split('=')[1])
        internet_acsess = 0
        secrkey_hash = hashpw(bytes(text[2].split('=')[1], 'utf-8'), salt=gensalt())
        description = text[3].split('=')[1]

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

        #  необходимая конечная ширина изображения вопроса
        required_width = 1730

        #  количество строк по варианту фиксировано, поэтому начинаю сразу со строк по вопросам
        i = 4
        try:
            for i in range(4, len(text)):
                #  если начался новый вопрос/информация, записываются в бд и сбрасываются в переменной собранные данные
                if text[i].startswith('I ') or text[i].startswith('Q'):
                    if len(quest_data) > 0:
                        database.new_quest(quest_data)
                    if text[i].startswith('I '):
                        quest_data = [("number", "Info")]
                    else:
                        quest_data = [("number", int(text[i].split()[0][1:]))]
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
                elif param[0] == 'SANS':
                    quest_data.append(("rows_in_answ", param[1].split(', ')[0]))
                    quest_data.append(("col_in_answ", param[1].split(', ')[1]))
                elif param[0] == 'SEP':
                    quest_data.append(("info", f"separator='{param[1]}'"))
                elif param[0] == 'ANSW':
                    quest_data.append(("answer", param[1]))
            #  запись последнего невошедшего вопроса
            database.new_quest(quest_data)
            self.logsTextEdit.setPlainText('')
        except Exception:
            self.logsTextEdit.setPlainText(f"Указанные файлы изображений ({text[i]}) не найдены")

        database.close()

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
