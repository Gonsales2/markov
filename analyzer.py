
import os
import sqlite3
from collections import Counter

CORPUS_FOLDER = "cleaned"
DB_PATH = "database/statistics.db"
MAX_CONTEXT = 13
CHUNK_SIZE = 100_000
BATCH_SIZE = 50_000
ALLOWED = set(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?")
os.makedirs("database", exist_ok=True)
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statistics (
            context TEXT NOT NULL,
            next_char TEXT NOT NULL,
            count INTEGER NOT NULL,
            PRIMARY KEY (context, next_char)
        )
    """)
    cursor.execute("DELETE FROM statistics")
    connection.commit()

def save_counts(cursor, connection, counts):
    if not counts:
        return
    cursor.executemany("""
        INSERT INTO statistics (context, next_char, count)
        VALUES (?, ?, ?)
        ON CONFLICT(context, next_char)
        DO UPDATE SET count = count + excluded.count
    """, [
        (context, char, count)
        for (context, char), count in counts.items()
    ])
    connection.commit()
    counts.clear()

def process_file(path, cursor, connection):
    counts = Counter()
    tail = ""
    with open(path, "r", encoding="utf-8") as file:
        while True:
            chunk = file.read(CHUNK_SIZE)
            if not chunk:
                break
            chunk = "".join(
                char if char in ALLOWED else " "
                for char in chunk.lower()
            )
            text = tail + chunk
            start = len(tail)
            for i in range(start, len(text)):
                next_char = text[i]
                counts[("", next_char)] += 1
                max_length = min(MAX_CONTEXT, i)
                for length in range(1, max_length + 1):
                    context = text[i - length:i]
                    counts[(context, next_char)] += 1
                if len(counts) >= BATCH_SIZE:
                    save_counts(cursor, connection, counts)
            tail = text[-MAX_CONTEXT:]
    save_counts(cursor, connection, counts)


def main():
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA synchronous=NORMAL")
    create_database(connection)
    cursor = connection.cursor()
    files = [
        filename
        for filename in os.listdir(CORPUS_FOLDER)
        if filename.lower().endswith(".txt")
    ]
    for filename in files:
        path = os.path.join(CORPUS_FOLDER, filename)
        print(f"Обрабатывается: {filename}")
        process_file(path, cursor, connection)
        print(f"Завершён: {filename}")
    connection.close()
    print("Подсчёт статистики завершён")


if __name__ == "__main__":
    main()
