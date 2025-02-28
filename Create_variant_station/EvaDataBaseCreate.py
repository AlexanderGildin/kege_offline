import sqlite3


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

    def clear_tables(self):  # удаляет записи из таблиц
        self.cur.execute("DELETE FROM Questions")
        self.cur.execute("DELETE FROM Variants")
        self.con.commit()

    def close(self):
        self.con.close()
