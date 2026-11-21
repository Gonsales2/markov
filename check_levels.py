import sqlite3

connection = sqlite3.connect(
    "file:database/statistics.db?mode=ro",
    uri=True
)

cursor = connection.cursor()

for length in range(14):
    context = "м" * length
    cursor.execute("""
        SELECT COUNT(*), SUM(count)
        FROM statistics
        WHERE context = ?
    """, (context,))
    variants, total = cursor.fetchone()
    print(
        f"Длина {length}: "
        f"вариантов = {variants}, "
        f"встречаемость = {total}"
    )

connection.close()