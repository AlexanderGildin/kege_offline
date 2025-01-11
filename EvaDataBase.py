import sqlite3
import pygame


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect('database.sqlite')
        self.cur = self.con.cursor()

    def make_new_db(self):
        with open('database.sql', 'r') as querytext:
            queries = querytext.read().split('\n')
        for query in queries:
            self.cur.execute(query)
        self.cur.execute('INSERT INTO Variants DEFAULT VALUES')
        self.con.commit()

    def new_quest(self, *fields_and_values):
        self.cur.execute(f"""INSERT INTO Questions ({", ".join(f"'{i[0]}'" for i in fields_and_values)})
         SET VALUES ({", ".join('?' * len(fields_and_values))})""", tuple(i[1] for i in fields_and_values))
        self.con.commit()

    def update_quests(self, ID, **fields_and_values):
        for field, value in fields_and_values.items():
            self.cur.execute(f"""UPDATE Questions SET '{field}' = '{value}' WHERE ID = {ID}""")
        self.con.commit()

    def update_variants(self, **fields_and_values):
        for field, value in fields_and_values.items():
            self.cur.execute(f"""UPDATE Variants SET '{field}' = '{value}'""")
        self.con.commit()

    def quest_image(self, ID):
        filebytes = self.cur.execute(f"SELECT question FROM Questions WHERE ID = {ID}").fetchone()
        with open('to_show_img.png', 'wb') as file:
            file.write(filebytes)
        image = pygame.image.load('to_show_img.png')
        return image

    def variant_info(self):
        keys = [i[0] for i in self.cur.execute("SELECT name FROM PRAGMA_TABLE_INFO('Variants')").fetchall()]
        values = self.cur.execute("SELECT * FROM Variants").fetchone()
        return {keys[i]:values[i] for i in range(len(keys))}

    def close(self):
        self.con.close()
