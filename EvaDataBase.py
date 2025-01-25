import sqlite3

import pygame


class DataBase:
    def __init__(self, dbname='database.db'):
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()

    def create_tables(self):  # создает таблицы если их нет
        with open('database.sql', 'r') as querytext:
            queries = querytext.read().split('\n')
        for query in queries:
            self.cur.execute(query)
        self.con.commit()

    def new_quest(self, fields_and_values: list):  # добавить новый вопрос
        self.cur.execute(f"""INSERT INTO Questions ({", ".join(f"'{i[0]}'" for i in fields_and_values)}) 
          VALUES ({", ".join('?' * len(fields_and_values))})""", tuple(i[1] for i in fields_and_values))
        self.con.commit()

    def update_quests(self, ID, **fields_and_values):  # обновить вопрос по ID
        for field, value in fields_and_values.items():
            self.cur.execute(f"""UPDATE Questions SET '{field}' = '{value}' WHERE ID = {ID}""")
        self.con.commit()

    def update_variants(self, **fields_and_values):  # обновить/записать вариант
        if self.cur.execute("SELECT * FROM Variants").fetchone() is None:
            self.cur.execute('INSERT INTO Variants DEFAULT VALUES')
            self.con.commit()
        for field, value in fields_and_values.items():
            self.cur.execute(f"""UPDATE Variants SET '{field}' = ?""", (value,))
        self.con.commit()

    def quest_image(self, ID) -> pygame.image:  # получить картинку вопроса как объект pygame.image по ID вопроса
        filebytes = self.cur.execute(f"SELECT question FROM Questions WHERE ID = {ID}").fetchone()[0]
        with open('to_show_img.png', 'wb') as file:
            file.write(filebytes)
        image = pygame.image.load('to_show_img.png')
        return image

    def variant_info(self) -> dict:  # вся информация по варианту - возвращает словарь "поле": "значение"
        keys = [i[0] for i in self.cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('Variants')").fetchall()]
        values = self.cur.execute("SELECT * FROM Variants").fetchone()
        return {keys[i]: values[i] for i in range(len(keys))}

    def close(self):
        self.con.close()

    def get_count_of_quest(self):
        return self.cur.execute("""SELECT count_of_quest FROM Variants""").fetchone()[0]

    def get_file_names(self):
        names = [str(i[0]).strip() for i in
                 self.cur.execute("SELECT files FROM Questions WHERE files IS NOT NULL").fetchall()]
        return names

    def quest_id_by_num(self, quest_num):
        if quest_num == 0:
            id = self.cur.execute(f"""SELECT id FROM Questions WHERE number = 'Info'""").fetchone()[0]
            return id
        id = self.cur.execute(f"""SELECT id FROM Questions WHERE number = {quest_num}""").fetchone()[0]
        return id

    def clear_tables(self):
        self.cur.execute("DELETE FROM Questions")
        self.cur.execute("DELETE FROM Variants")
        self.con.commit()

    def get_rows_and_cols(self) -> dict:  # возвращает словать {номер вопроса: (строки, колонки)}
        quests = self.cur.execute("""SELECT number, rows_in_answ, col_in_answ 
        FROM Questions WHERE number != 'Info'""").fetchall()
        return {int(quest[0]): (int(quest[1]), int(quest[2])) for quest in quests}
