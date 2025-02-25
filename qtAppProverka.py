import csv
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from proverka_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.run)
        self.setWindowTitle("Сверка результатов")

    def run(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if folder_path:
            output_dir = "reports"
            os.makedirs(output_dir, exist_ok=True)
            report_path = os.path.join(output_dir, "final.txt")
            with open(report_path, 'w', encoding='utf-8') as report:
                report.write("") 

            txt_files = [os.path.join(root, file)
                         for root, _, files in os.walk(folder_path)
                         for file in files if file.lower().endswith(".txt")]

            if not txt_files:
                print("Нет файлов .txt в папке")
                self.label.setText("Нет файлов .txt в папке")
                return

            for file_path in txt_files:
                variant_number = self.extract_variant(file_path)
                print(f"{file_path} → Вариант: {variant_number}")
                if variant_number:
                    db_path = f"{folder_path}\\database_{variant_number}.db"
                    if os.path.exists(db_path):
                        self.process_file(file_path, db_path)
                    else:
                        print(f"База данных {db_path} не найдена")
                        self.label.setText(f"База данных {db_path} не найдена")
                else:
                    print(f"Не удалось извлечь номер варианта из файла {file_path}")
                    self.label.setText(f"Не удалось извлечь номер варианта из файла {file_path}")

    def extract_variant(self, file_path):
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                lines = file.readlines()[:3] 

            for line in lines:
                words = line.split()
                for i, word in enumerate(words):
                    if "вар" in word.lower() and i + 1 < len(words):
                        try:
                            return int(words[i + 1]) 
                        except ValueError:
                            continue 
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")
            
        
        return None 

    def process_file(self, student_file, db_path):
        variant_number, student_answers = self.read_student_answers(student_file)
        correct_answers = self.get_correct_answers(db_path)
        results, total_score = self.compare_answers(student_answers, correct_answers)
        self.generate_report(student_file, results, total_score)

    def read_student_answers(self, file_path):
        with open(file_path, 'r', encoding='cp1251') as file:
            lines = file.readlines()

        variant_number = int(lines[0].strip().split()[-1])  
        answers = []

        for line in lines[2:]: 
            parts = line.split(". ", 1) 
            if len(parts) > 1:
                answers.append(parts[1].strip()) 
            else:
                answers.append("_")

        return variant_number, answers

    def get_correct_answers(self, db_path):
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT number, answer, points FROM Questions")
        correct_answers = {int(row[0]): (row[1], int(row[2]) if row[2] is not None else 0) for row in cursor.fetchall()}
        connection.close()
        return correct_answers

    def compare_answers(self, student_answers, correct_answers):
        total_score = 0
        results = []
        for i, student_answer in enumerate(student_answers, start=1):
            correct_answer, points = correct_answers.get(i, (None, 0))
            is_correct = student_answer == correct_answer
            results.append((i, student_answer, is_correct, points if is_correct else 0))
            total_score += points if is_correct else 0
        return results, total_score

    def generate_report(self, student_file, results, total_score, output_dir="reports"):
        os.makedirs(output_dir, exist_ok=True)
        report_txt_path = os.path.join(output_dir, "final.txt")
        report_csv_path = os.path.join(output_dir, "final.csv")

        student_name = os.path.splitext(os.path.basename(student_file))[0]

        #TXT
        with open(report_txt_path, 'a', encoding='utf-8') as report:
            report.write(f"Отчёт для {student_name}\nИтоговый балл: {total_score}\n\n")
            
            for question_id, answer, is_correct, points in results:
                status = "Правильно" if is_correct else "Неправильно"
                if ";" in answer: 
                    parts = answer.split(";")
                    for idx, part in enumerate(parts, start=1):
                        report.write(f"Вопрос {question_id}p{idx}: {part.strip()} - {status} (+{points} баллов)\n")
                else:
                    report.write(f"Вопрос {question_id}: {answer.strip()} - {status} (+{points} баллов)\n")

            report.write("\n" + "=" * 50 + "\n\n")
        #CSV
        existing_data = []
        if os.path.exists(report_csv_path):
            with open(report_csv_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                existing_data = list(reader)

        headers = ["Имя ученика", "Итоговый балл"]
        expanded_questions = set()

        for q_id, answer, _, _ in results:
            parts = answer.split(";") if ";" in answer else [answer]  
            for idx in range(1, len(parts) + 1):
                expanded_questions.add(f"{q_id}p{idx}")

        sorted_questions = sorted(expanded_questions, key=lambda x: (int(x.split('p')[0]), x))
        headers.extend(sum(([q, f"{q} Баллы"] for q in sorted_questions), []))  

        if existing_data:
            existing_headers = existing_data[0]
            for new_header in headers:
                if new_header not in existing_headers:
                    existing_headers.append(new_header)  
            existing_data[0] = existing_headers  
        else:
            existing_data.append(headers) 

        
        student_row = [student_name, str(total_score)]
        answers_dict = {}

        for q_id, answer, _, _ in results:
            parts = answer.split(";") if ";" in answer else [answer] 
            for idx, part in enumerate(parts, start=1):
                key = f"{q_id}p{idx}"
                answers_dict[key] = part.strip()

        for column in existing_data[0][2:]: 
            student_row.append(answers_dict.get(column, "_")) 

        existing_data.append(student_row)

        with open(report_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerows(existing_data)
        self.label.setText(f"отчёт сохранён в {output_dir}")

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()