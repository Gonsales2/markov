import sqlite3

connection = sqlite3.connect("database/statistics.db")
cursor = connection.cursor()

context = "привет"

cursor.execute("""
    SELECT next_char, count
    FROM statistics
    WHERE context = ?
    ORDER BY count DESC
""", (context,))

rows = cursor.fetchall()

total = sum(count for char, count in rows)

print(f"Контекст: {context}")
print(f"Всего продолжений: {total}")

for char, count in rows:
    probability = count / total
    print(f"{repr(char)}: {count}, P = {probability:.6f}")

connection.close()