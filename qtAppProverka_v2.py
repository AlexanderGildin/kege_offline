import csv
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from proverka_ui_v2 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.checkBox_4.clicked.connect(self.Rename)
        self.setWindowTitle("Сверка результатов")

    def run(self):

        global f_csv, f_txt, first_run
        first_run = True
        if self.checkBox_4.isChecked() == True:
            folder_path = os.getcwd()
        else:
            folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            try: #ПРАВКА А.Г.
                output_dir = "reports"
                os.makedirs(output_dir, exist_ok=True)
            except:
                print(f"Ошибка создания папки reports в текущей папке")
                self.label.setText("Ошибка создания папки reports в текущей папке")
                return

            txt_files = [os.path.join(root, file)
                         for root, _, files in os.walk(folder_path)
                         for file in files if file.lower().endswith(".txt")]
            if self.checkBox_2.isChecked():
                f_txt = open(output_dir + "\\final.txt", "w", encoding="utf-8")
            if self.checkBox_3.isChecked():
                f_csv = open(output_dir + "\\final.csv", "w", encoding="utf-8")


            if not txt_files:
                print("Нет файлов .txt в папке")
                self.label.setText("Нет файлов ответов (.txt) в выбранном каталоге")
                return

            for file_path in txt_files:
                if "fio" not in file_path: #ПРАВКА А.Г.
                    continue
                variant_number = self.extract_variant(file_path)
                print(f"{file_path} → Вариант: {variant_number}")
                if variant_number:
                    db_path = f"{folder_path}\\{variant_number}_ans.db" #ПРАВКА А.Г.
                    # db_path = f"{folder_path}\\database_{variant_number}.db"
                    if os.path.exists(db_path):
                        self.process_file(file_path, db_path)
                    else:
                        print(f"База данных  с ответами для варианта {variant_number} ({db_path})  не найдена") #ПРАВКА А.Г.
                        self.label.setText(f"База данных {db_path} не найдена")
                else:
                    # ПРАВКА А.Г.
                    continue
            if self.checkBox_2.isChecked():
                f_txt.close()
            if self.checkBox_3.isChecked():
                f_csv.close()
                    # print(f"Не удалось извлечь номер варианта из файла {file_path}")
                    # self.label.setText(f"Не удалось извлечь номер варианта из файла {file_path}")
            
    def Rename(self):
        if self.checkBox_4.isChecked() == True:
            self.pushButton.setText("Проверить")
        else:
            self.pushButton.setText("Выбрать каталог")

    def extract_variant(self, file_path):
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                lines = file.readlines()[:3] 
            return lines[0].rstrip() #ПРАВКА А.Г.

        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")
            
        
        return None 

    def process_file(self, student_file, db_path):
        variant_number, student_answers, data_of_test = self.read_student_answers(student_file)
        correct_answers = self.get_correct_answers(db_path)
        results, total_score = self.compare_answers(student_answers, correct_answers)
        self.generate_report(student_file, results, total_score, data_of_test, variant_number)

    def read_student_answers(self, file_path):
        with open(file_path, 'r', encoding='cp1251') as file:
            lines = file.readlines()

        variant_number = int(lines[0].strip().split()[-1]) 
        data_of_test = lines[1].rstrip()
        answers = []

        for line in lines[2:]: 
            if line.strip() == '':
                continue
            parts = line.split(". ", 1) 
            if len(parts) > 1:
                answers.append(parts[1].strip()) 
            else:
                answers.append("_")

        return variant_number, answers, data_of_test

    def get_correct_answers(self, db_path):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT number, answer, points FROM Questions")
        
        correct_answers = {}
        
        for row in cursor.fetchall():
            question_number = int(row[0])
            answers = row[1].split(";") 
            points = int(row[2]) if row[2] is not None else 0
            
            correct_answers[question_number] = (answers, points) 

        connection.close()
        return correct_answers

    def compare_answers(self, student_answers, correct_answers):
        total_score = 0
        results = []

        for i, student_answer in enumerate(student_answers, start=1):
            correct_answer_set, points = correct_answers.get(i, (set(), 0))



            student_answer_set = student_answer.split(";") if student_answer != "_" else []
            print(student_answer_set)
            if len(correct_answer_set) == 1:
                try:
                    is_correct = student_answer_set[0] == correct_answer_set[0]
                    results.append((i, student_answer_set[0], is_correct, points if is_correct else 0))
                    total_score += points if is_correct else 0
                except:
                    pass
            else:
                for j in range(len(correct_answer_set)):
                    if j + 1 <= len(student_answer_set):
                        is_correct = student_answer_set[j] == correct_answer_set[j]
                        results.append((f"{i}-{j + 1}", student_answer_set[j], is_correct, points / len(correct_answer_set) if is_correct else 0))
                    else:
                        is_correct = False
                        results.append((f"{i}-{j + 1}", "-", is_correct, points / len(correct_answer_set) if is_correct else 0))
                    total_score += points / len(correct_answer_set) if is_correct else 0
            
            

        print(results)
        return results if results else [], total_score if total_score > 0 else 0



    def generate_report(self, student_file, results, total_score, data_of_test, variant_numb, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)
        report_txt_path = os.path.join(output_dir, "final.txt")
        report_csv_path = os.path.join(output_dir, "final.csv")
        global f_txt, f_csv, first_run
        student_name = os.path.splitext(os.path.basename(student_file))[0]

        #TXT
        if self.checkBox_2.isChecked() == True:

                f_txt.write(f"Отчёт для {student_name}\nИтоговый балл: {total_score}\n\n Дата написанния {data_of_test}\n\n Вариант {variant_numb}\n\n")
                for question_id, answer, is_correct, points in results:
                    status = "Правильно" if is_correct else "Неправильно"
                    # if ";" in answer: 
                    #     parts = answer.split(";")
                    #     for idx, part in enumerate(parts, start=1):
                    #         report.write(f"{question_id}-{idx} {part.strip()} - {status} (+{points} баллов)\n")
                    # else:
                    f_txt.write(f"{question_id} {answer.strip()} - {status} (+{points} баллов)\n")

                f_txt.write("\n" + "=" * 50 + "\n\n")
        #CSV

        if self.checkBox_3.isChecked() == True:
                # report.write(f"Отчёт для {student_name}\nИтоговый балл: {total_score}\n\n")
                if first_run:
                    first_string = f"Имя;Дата тестирования;Вариант;Сумма баллов"
               
                    for question_id, answer, is_correct, points in results:
                        first_string += ";" + str(question_id)
                    f_csv.write(first_string + "\n")
                    if not self.checkBox.isChecked():

                        first_run = False
                stroka = f"{student_name};{data_of_test};{variant_numb};{f"{total_score:0.2f}"}"
            

                for question_id, answer, is_correct, points in results:
                    stroka += ";" + str(points)
                    # status = "Правильно" if is_correct else "Неправильно"
                    # if ";" in answer: 
                    #     parts = answer.split(";")
                    #     for idx, part in enumerate(parts, start=1):
                    #         report.write(f"{question_id}-{idx} {part.strip()} - {status} (+{points} баллов)\n")
                    # else:
                    #     report.write(f"{question_id} {answer.strip()} - {status} (+{points} баллов)\n")

                f_csv.write(stroka + "\n")
            



if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()