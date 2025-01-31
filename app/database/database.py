import sqlite3
from datetime import datetime


def init_db():
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS medications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            name TEXT NOT NULL,
            time TEXT NOT NULL
        )
        """)
        conn.commit()

def debug():
    conn = None
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM medications")
        data = cursor.fetchall()
        for record in data:
            print(record)
    except sqlite3.ProgrammingError as e:
        print(f"[ERROR] Ошибка при отладке базы данных: {e}")
    finally:
        if conn:
            conn.close()



def add_medication(user_id: str, name: str, time: str):
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO medications (user_id, name, time)
        VALUES(?,?,?)
        """, (user_id, name, time))
        conn.commit()

def get_medications(user_id: str):
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT id, name, time FROM medications WHERE user_id = ?
        """, (user_id,))
        medications = cursor.fetchall()
        return medications  # исправляем, удаляем второй вызов fetchall

def delete_medication(medication_id: int):
    with sqlite3.connect("db.sqlite3") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM medications WHERE id = ?
        """, (medication_id,))
        conn.commit()

def get_reminders():
    try:
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%H:%M")
        print(f"[DEBUG] Текущее время: {current_time}")
        cursor.execute("SELECT user_id, name FROM medications WHERE time = ?", (current_time,))
        reminders = cursor.fetchall()
        print(f"[DEBUG] Напоминания: {reminders}")
        return reminders
    except sqlite3.ProgrammingError as e:
        print(f"[ERROR] Ошибка базы данных: {e}")
    finally:
        conn.close()

