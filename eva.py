import sqlite3
import pygame


def save_file(DBname, filename):
    con = sqlite3.connect(DBname)
    cur = con.cursor()

    with open(filename, 'rb') as file:
        filebytes = file.read()
    cur.execute("INSERT INTO table (file, filename) VALUES (?, ?)", (filebytes, filename))
    con.commit()
    con.close()

def read_file(DBname, id):
    con = sqlite3.connect(DBname)
    cur = con.cursor()

    filebytes, filename = cur.execute(f"SELECT file, filename FROM table WHERE file_id = {id}").fetchone()
    with open(filename, 'wb') as file:
        file.write(filebytes)
    con.close()
    image = pygame.image.load(filename)
    return image