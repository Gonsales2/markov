import sqlite3
import random

DB_PATH = "database/statistics.db"
MAX_CONTEXT = 13

ALLOWED = set(
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюя .,!?"
)


def clean_text(text):
    text = text.lower()
    return "".join(
        char if char in ALLOWED else " "
        for char in text
    )


def get_next_char(cursor, text):
    max_length = min(MAX_CONTEXT, len(text))
    for length in range(max_length, -1, -1):
        if length == 0:
            context = ""
        else:
            context = text[-length:]
        cursor.execute("""
            SELECT next_char, count
            FROM statistics
            WHERE context = ?
        """, (context,))
        rows = cursor.fetchall()
        if rows:
            chars = [row[0] for row in rows]
            weights = [row[1] for row in rows]
            return random.choices(
                chars,
                weights=weights,
                k=1
            )[0]
    return None


def generate_text(cursor, start_text, length):
    text = clean_text(start_text)
    for i in range(length):
        next_char = get_next_char(cursor, text)
        if next_char is None:
            break
        text += next_char
    return text


def main():
    connection = sqlite3.connect(
        f"file:{DB_PATH}?mode=ro",
        uri=True
    )
    cursor = connection.cursor()
    print("Генератор текста на цепях Маркова")
    start_text = input("Введите начало текста: ")
    length = int(input("Количество новых символов: "))
    result = generate_text(cursor, start_text, length)
    print("\nСгенерированный текст:\n")
    print(result)
    connection.close()


if __name__ == "__main__":
    main()