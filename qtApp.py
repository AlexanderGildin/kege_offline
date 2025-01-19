from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton,
    QWidget, QFileDialog, QMessageBox
)
import os
from add_question import AddQuestionWindow  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QT Редактор вариантов")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        self.create_test_button = QPushButton("Создать тест")
        self.add_question_button = QPushButton("Добавить вопрос")
        self.run_test_button = QPushButton("Пройти тест")
        self.exit_button = QPushButton("Выход")

        self.create_test_button.clicked.connect(self.create_test)
        self.add_question_button.clicked.connect(self.open_add_question_window)
        self.run_test_button.clicked.connect(self.run_test)
        self.exit_button.clicked.connect(self.close)

        layout.addWidget(self.create_test_button)
        layout.addWidget(self.add_question_button)
        layout.addWidget(self.run_test_button)
        layout.addWidget(self.exit_button)

        self.central_widget.setLayout(layout)

        self.current_test_file = None

    def create_test(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить тест", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            try:
                with open(file_name, 'w') as f:
                    f.write("1\nMAXTIME=0\nKEY=\nDESCRIPTION=\n")  
                QMessageBox.information(self, "Успех", "Файл теста создан.")
                self.current_test_file = file_name  
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать файл: {e}")

    def open_add_question_window(self):
        if not self.current_test_file:
            QMessageBox.warning(
                self, "Внимание", "Сначала создайте или выберите файл теста."
            )
            return

        self.add_question_window = AddQuestionWindow(self.current_test_file)
        self.add_question_window.show()

    def run_test(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Выбрать тест", "", "Text Files (*.txt);;All Files (*)"
        )
        if file_name:
            if os.path.exists(file_name):
                QMessageBox.information(self, "Информация", f"Выбран файл теста: {file_name}")
            else:
                QMessageBox.critical(self, "Ошибка", "Файл не существует.")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
