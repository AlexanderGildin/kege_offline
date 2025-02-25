from PyQt6.QtWidgets import QApplication, QMainWindow, QScrollArea
from QtRedactorUI import Ui_MainWindow
from EvaDataBaseCreate import DataBase
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
        self.setWindowTitle("QT Р РµРґР°РєС‚РѕСЂ РІР°СЂРёР°РЅС‚РѕРІ")

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
        secrkey_hash = ''
        max_time_min = '' # С‚Р°Рј РїСЂРµРґРїРѕР»Р°РіР°РµС‚СЃСЏ int
        internet_acsess = 0

        #  РїРѕР»СѓС‡РµРЅРёРµ РїР°СЂР°РјРµС‚СЂРѕРІ РІР°СЂРёР°РЅС‚Р°
        for i in range(8):
            if text[i].startswith('COUNT_OF_QUESTIONS'):
                count_of_quest = int(text[i].split('=')[1])
            if text[i].startswith('MAXTIME'):
                if len(text[1].split('=')[1]) > 0 and text[1].split('=')[1] != '0':
                    max_time_min = int(text[1].split('=')[1])
            if text[i].startswith('KEY'):
                if len(text[2].split('=')[1]) > 0:
                    secrkey_hash = hashpw(bytes(text[2].split('=')[1], 'utf-8'), salt=gensalt())
            if text[i].startswith('DESCRIPTION'):
                description = text[i].split('=')[1]
            if text[i].startswith('INTERNET_ACCESS'):
                if text[i].split('=')[1]=='1':
                    internet_acsess = 1
        database = DataBase(description + '.db')
        DB_with_ans = DataBase(f"{description}_ans.db")
        database.create_tables()
        DB_with_ans.create_tables()

        #  Р·Р°РїРёСЃСЊ РІР°СЂРёР°РЅС‚Р°
        database.update_variants(
            description=description,
            count_of_quest=count_of_quest,
            max_time_min=max_time_min,
            internet_acsess=internet_acsess,
            secrkey_hash=secrkey_hash
        )

        #  РїРѕСЃР»РµРґРѕРІР°С‚РµР»СЊРЅР°СЏ Р·Р°РїРёСЃСЊ РІРѕРїСЂРѕСЃРѕРІ:

        # quest_data - РїРµСЂРµРјРµРЅРЅР°СЏ СЃРѕ Р·РЅР°С‡РµРЅРёСЏРјРё С‚РµРєСѓС‰РµРіРѕ РІРѕРїСЂРѕСЃР°/РёРЅС„РѕСЂРјР°С†РёРё
        quest_data = []
        ans_data = []

        #  РЅРµРѕР±С…РѕРґРёРјР°СЏ РєРѕРЅРµС‡РЅР°СЏ С€РёСЂРёРЅР° РёР·РѕР±СЂР°Р¶РµРЅРёСЏ РІРѕРїСЂРѕСЃР°
        required_width = 1730

        #  РєРѕР»РёС‡РµСЃС‚РІРѕ СЃС‚СЂРѕРє РїРѕ РІР°СЂРёР°РЅС‚Сѓ С„РёРєСЃРёСЂРѕРІР°РЅРѕ, РїРѕСЌС‚РѕРјСѓ РЅР°С‡РёРЅР°СЋ СЃСЂР°Р·Сѓ СЃРѕ СЃС‚СЂРѕРє РїРѕ РІРѕРїСЂРѕСЃР°Рј
        i = 4
        try:
            for i in range(5, len(text)):
                #  РµСЃР»Рё РЅР°С‡Р°Р»СЃСЏ РЅРѕРІС‹Р№ РІРѕРїСЂРѕСЃ/РёРЅС„РѕСЂРјР°С†РёСЏ, Р·Р°РїРёСЃС‹РІР°СЋС‚СЃСЏ РІ Р±Рґ Рё СЃР±СЂР°СЃС‹РІР°СЋС‚СЃСЏ РІ РїРµСЂРµРјРµРЅРЅРѕР№ СЃРѕР±СЂР°РЅРЅС‹Рµ РґР°РЅРЅС‹Рµ
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

                #  РѕР±СЂР°Р±РѕС‚РєР° РІРѕР·РјРѕР¶РЅС‹С… РїРѕР»РµР№ Рё РґРѕР±Р°РІР»РµРЅРёРµ РёС… Р·РЅР°С‡РµРЅРёР№ РІ quest_data
                if param[0] == 'IMG':
                    lname = param[1].replace(' ','')
                    lname = lname.replace(';',',')
                    image_size_changes(lname.split(','), required_width, result_file_name='questImg.png')
                    with open('questImg.png', 'rb') as image:
                        quest_bytes = image.read()
                    quest_data.append(("question", quest_bytes))

                elif param[0] == 'FILES':
                    lifn = param[1].replace(" ",'')
                    lifn = lifn.replace(',',';')
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
                    quest_data.append(('points', param[1]))
                elif param[0] == 'SEP':
                    ans_data.append(("info", f"separator='{param[1]}'"))
                elif param[0] == 'ANSW':
                    ans_data.append(("answer", param[1]))
            #  Р·Р°РїРёСЃСЊ РїРѕСЃР»РµРґРЅРµРіРѕ РЅРµРІРѕС€РµРґС€РµРіРѕ РІРѕРїСЂРѕСЃР°
            database.new_quest(quest_data)
            DB_with_ans.new_quest(ans_data)
            self.logsTextEdit.setPlainText('Р›РѕРі:')
        except:
            pass

        database.close()
        files.append(f'{description}.db')
        for x in files:
            shutil.copy(x, str(os.getcwd() + r'\files'+"\\"+x)) #Р—РђРњР•РќРРўР¬ РќРђ MOVE
        shutil.make_archive(f'{description}', 'zip', root_dir='files') #РџРѕС…РѕР¶Рµ, С‡С‚Рѕ СЃРѕР·РґР°РµС‚ РґР°Р¶Рµ РµСЃР»Рё С‚Р°РєРѕР№ Р±С‹Р» СѓР¶Рµ
        try:
            os.rename(f'{description}.zip', f'{description}.tsk')
        except:
            os.remove(f'{description}.tsk')
            os.rename(f'{description}.zip', f'{description}.tsk')
        self.logsTextEdit.setPlainText('Р’Р°СЂРёР°РЅС‚ СЃРѕР·РґР°РЅ')

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
                error_output.append('РћС€РёР±РєР°: РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ СЃС‚СЂРѕРєР°: COUNT_OF_QUESTIONS=')
            if flag_description:
                error_output.append('РћС€РёР±РєР°: РѕС‚СЃСѓС‚СЃС‚РІСѓРµС‚ СЃС‚СЂРѕРєР°: DESCRIPTION=')
            for i in range(len(text)):
                #  РµСЃР»Рё РЅР°С‡Р°Р»СЃСЏ РЅРѕРІС‹Р№ РІРѕРїСЂРѕСЃ/РёРЅС„РѕСЂРјР°С†РёСЏ, Р·Р°РїРёСЃС‹РІР°СЋС‚СЃСЏ РІ Р±Рґ Рё СЃР±СЂР°СЃС‹РІР°СЋС‚СЃСЏ РІ РїРµСЂРµРјРµРЅРЅРѕР№ СЃРѕР±СЂР°РЅРЅС‹Рµ РґР°РЅРЅС‹Рµ
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
                #  РѕР±СЂР°Р±РѕС‚РєР° РІРѕР·РјРѕР¶РЅС‹С… РїРѕР»РµР№ Рё РґРѕР±Р°РІР»РµРЅРёРµ РёС… Р·РЅР°С‡РµРЅРёР№ РІ quest_data
                if self.param[0].startswith('Q'):
                    self.q_num = self.param[0].split()[0][1:]
                    self.question_number_q = self.q_num
                    q_num_list.append(self.q_num)
                if self.param[0] == 'IMG_I':
                    try:
                        if len(self.param[1].split()) != 0:
                            flag_img_i = True
                            for x in self.param[1].split(';'):
                                self.sep_img_i = ';'
                                if os.path.exists(os.path.dirname(__file__)+"\\"+x) == False:
                                    for y in self.param[1].split(','):
                                        self.sep_img_i = ','
                                        if os.path.exists(os.path.dirname(__file__)+"\\"+y) == False:
                                            flag_img_i = False
                        if len(self.param[1]) != 0 or self.param[0].startswith('Q') and flag_img_i:
                            image_size_changes(self.param[1].split(self.sep_img_i), self.required_width,
                                               result_file_name='questImg.png')
                        else:
                            error_output.append(
                                str("РћС€РёР±РєР°" + f": РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹"))
                    except FileNotFoundError:
                        error_output.append(
                            str("РћС€РёР±РєР°" + f": РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹"))
                if self.param[0] == 'IMG':
                    try:
                        if len(self.param[1].split()) != 0:
                            flag_img = True
                            for x in self.param[1].split(';'):
                                self.sep_img = ';'
                                if os.path.exists(os.path.dirname(__file__)+"\\"+x) == False:
                                    for y in self.param[1].split(','):
                                        self.sep_img = ','
                                        if os.path.exists(os.path.dirname(__file__)+"\\"+y) == False:
                                            flag_img = False
                        # if len(self.param[1]) != 0 or self.param[0].startswith('Q') and flag_img:
                        #     image_size_changes(self.param[1].split(self.sep_img), self.required_width,
                        #                        result_file_name='questImg.png')
                        else:
                            error_output.append(
                                str("РћС€РёР±РєР° (РІ Q" + str(
                                    self.q_num) + f"): РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹"))
                    except FileNotFoundError:
                        error_output.append(
                            str("РћС€РёР±РєР° (РІ Q" + str(
                                self.q_num) + f"): РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹"))
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
                                if os.path.exists(os.path.dirname(__file__)+"\\"+x) == False:
                                    for y in self.param[1].split(','):
                                        self.sep_files = ','
                                        if os.path.exists(os.path.dirname(__file__)+"\\"+y) == False:
                                            error_output.append(str('РћС€РёР±РєР° (РІ Q' +
                                                                    str(self.q_num)
                                                                    + f'): РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹'))
                    except FileNotFoundError:
                        error_output.append(str('РћС€РёР±РєР° (РІ Q' +
                                                str(self.q_num)
                                                + f'): РЈРєР°Р·Р°РЅРЅС‹Рµ С„Р°Р№Р»С‹ РёР·РѕР±СЂР°Р¶РµРЅРёР№ {text[i]} РЅРµ РЅР°Р№РґРµРЅС‹'))
                if self.param[0] == 'ANSW':
                    if (len(self.param[1].split(separator)) != number_of_questions or self.param[1] == ''
                            and number_of_questions != 0):
                        error_output.append(str('РћС€РёР±РєР° (РІ Q' +
                                                str(self.q_num)
                                                + '): РќРµ СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ РєРѕР»РёС‡РµСЃС‚РІРѕ РѕС‚РІРµС‚РѕРІ ANSW='))
                        #  raise NoResponse
                    else:
                        answer_list.append(self.param[1].split(separator))
            self.logsTextEdit.setPlainText('РћРљ')
        except Exception:
            error_output.append('РќРµРёР·РІРµСЃС‚РЅР°СЏ РѕС€РёР±РєР° РІ РІРѕРїСЂРѕСЃРµ Q' + str(self.q_num))
        if int(self.q_num) != int(self.count_of_question):
            error_output.append('РћС€РёР±РєР°: РЅРµ СЃРѕРІРїР°РґР°РµС‚ РєРѕР»РёС‡РµСЃС‚РІРѕ РІРѕРїСЂРѕСЃРѕРІ')
        for x in q_num_list:
            if int(x) > self.count_of_question or len(set(q_num_list)) != len(q_num_list):
                error_output.append('РћС€РёР±РєР°: РЅРµРїСЂР°РІРёР»СЊРЅР°СЏ РЅСѓРјРµСЂР°С†РёСЏ РІРѕРїСЂРѕСЃРѕРІ')
                break
        if len(error_output) > 0:
            self.logsTextEdit.setPlainText('\n'.join(error_output))
        if len(error_output) == 0:
            self.insertVariant()

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