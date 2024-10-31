import json

from yandex_reviews_parser.utils import YandexParser

id_ya = 1713775878  # ID компании
parser = YandexParser(id_ya)
all_data = parser.parse()  # Получаем все данные
names = [review["name"] for review in all_data.get("company_reviews", [])]

# Записываем имена в JSON файл
with open("yandex_names.json", "w", encoding="utf-8") as data:
    json.dump({"names": names}, data, indent=4, ensure_ascii=False)
