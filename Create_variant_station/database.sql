--
-- ���� ������������ � ������� SQLiteStudio v3.4.12 � �� ��� 28 19:43:43 2024
--
-- �������������� ��������� ������: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- �������: Questions
CREATE TABLE IF NOT EXISTS Questions (ID INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, question BLOB, files TEXT, rows_in_answ INTEGER, col_in_answ INTEGER, answer TEXT, info TEXT, points TEXT);

-- �������: Variants
CREATE TABLE IF NOT EXISTS Variants (description TEXT, count_of_quest INTEGER, max_time_min INTEGER, internet_acsess INTEGER, secrkey_hash TEXT, info TEXT);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
