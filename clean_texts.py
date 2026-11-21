
import os
import re


def read_text(path):
    with open(path, "rb") as file:
        data = file.read()
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("cp1251")
    
INPUT_FOLDER = "corpus"
OUTPUT_FOLDER = "cleaned"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
pattern = re.compile(r"[^а-яё.,!? ]")
for filename in os.listdir(INPUT_FOLDER):
    if not filename.endswith(".txt"):
        continue
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    text = read_text(input_path)
    text = text.lower()
    text = pattern.sub("", text)
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Обработан файл: {filename}")
print("Обработка завершена")
