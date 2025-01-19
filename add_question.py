from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QPushButton, QMessageBox
)


class AddQuestionWindow(QDialog):
    def __init__(self, test_file):
        super().__init__()
        self.test_file = test_file
        self.setWindowTitle("Добавить вопрос")
        self.setGeometry(200, 200, 400, 300)

        form_layout = QFormLayout()

        self.type_input = QComboBox()
        self.type_input.addItems(["Q (Вопрос)", "I (Информация)"])
        self.number_input = QLineEdit()
        self.img_input = QLineEdit()
        self.files_input = QLineEdit()
        self.sans_input = QLineEdit()
        self.sep_input = QLineEdit()
        self.answ_input = QLineEdit()

        form_layout.addRow("Тип экрана", self.type_input)
        form_layout.addRow("Номер экрана/вопроса", self.number_input)
        form_layout.addRow("IMG (изображения)", self.img_input)
        form_layout.addRow("FILES (файлы)", self.files_input)
        form_layout.addRow("SANS (строки, столбцы)", self.sans_input)
        form_layout.addRow("SEP (разделитель)", self.sep_input)
        form_layout.addRow("ANSW (ответы)", self.answ_input)

        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_question)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_question(self):
        q_type = self.type_input.currentText()[0]
        number = self.number_input.text()
        img = self.img_input.text()
        files = self.files_input.text()
        sans = self.sans_input.text() or "1,1"
        sep = self.sep_input.text() or ";"
        answ = self.answ_input.text()

        if not number.isdigit():
            QMessageBox.warning(self, "Ошибка", "Номер экрана/вопроса должен быть числом.")
            return

        if not img:
            QMessageBox.warning(self, "Ошибка", "Поле IMG обязательно.")
            return

        if q_type == "Q" and not answ:
            QMessageBox.warning(self, "Ошибка", "Для вопросов необходимо указать ответы.")
            return

        try:
            with open(self.test_file, 'a') as f:
                f.write(
                    f"{q_type}{number} {img}\n"
                    f"IMG={img}\n"
                    f"FILES={files}\n"
                    f"SANS={sans}\n"
                    f"SEP={sep}\n"
                    f"ANSW={answ}\n"
                )
            QMessageBox.information(self, "Успех", "Вопрос успешно добавлен.")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить вопрос: {e}")
