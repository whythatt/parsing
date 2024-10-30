# Функция для чтения никнеймов из файла
def read_nicks(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file if line.strip())


# Функция для чтения ников и номеров из второго файла
def read_nicks_and_numbers(file_path):
    nicks_and_numbers = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            parts = (
                line.strip().split()
            )  # Предполагаем, что ник и номер разделены пробелом
            if len(parts) == 2:
                nicks_and_numbers[parts[0]] = parts[1]  # Сохраняем в словаре
    return nicks_and_numbers


# Функция для записи совпадений в третий файл
def write_matches(matches, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        for nick, number in matches:
            file.write(f"{nick} {number}\n")


# Основной код
def main():
    # Путь к вашим файлам
    nicks_file = "only_nicks.txt"  # Файл с никами пользователей
    nicks_and_numbers_file = "pikabu_ru_base_osina.txt"  # Файл с никами и номерами
    output_file = "matches.txt"  # Файл для записи совпадений

    # Чтение данных из файлов
    user_nicks = read_nicks(nicks_file)
    nicks_with_numbers = read_nicks_and_numbers(nicks_and_numbers_file)

    # Поиск совпадений
    matches = [
        (nick, nicks_with_numbers[nick])
        for nick in user_nicks
        if nick in nicks_with_numbers
    ]

    # Запись совпадений в выходной файл
    write_matches(matches, output_file)


if __name__ == "__main__":
    main()
