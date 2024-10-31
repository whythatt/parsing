import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Настройка драйвера
driver = webdriver.Chrome()  # Убедитесь, что chromedriver находится в PATH

# URL для загрузки
# url = "https://pikabu.ru/community/Bank/search?t=%D0%91%D0%B0%D0%BD%D0%BA&st=2"
# driver.get(url)

# Прокрутка страницы вниз для подгрузки постов
# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Явное ожидание загрузки новых постов
#     WebDriverWait(driver, 50).until(
#         lambda d: d.execute_script("return document.readyState") == "complete"
#     )
#
#     time.sleep(5)
#
#     # Получаем новую высоту страницы
#     new_height = driver.execute_script("return document.body.scrollHeight")
#
#     if new_height == last_height:
#         break  # Прокрутка завершена, если высота не изменилась
#
#     last_height = new_height
#
# # Получаем HTML-код страницы после загрузки всех постов
# page_source = driver.page_source
# soup = BeautifulSoup(page_source, "html.parser")
#
# # Извлечение всех ссылок на комментарии
# comment_links = soup.find_all("a", class_="story__comments-link story__to-comments")
# links_list = [link["href"] for link in comment_links]

comments_list = []
# Параллельная обработка ссылок на комментарии
with open("links_list.txt", "r") as links_list:
    for link in links_list:
        driver.get(link)

        # Ожидание кнопки "Показать все комментарии" и клик по ней
        wait = WebDriverWait(driver, 50)
        show_comments_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "comment__more"))
        )
        ActionChains(driver).move_to_element(show_comments_button).click().perform()

        # Ожидание подгрузки комментариев
        WebDriverWait(driver, 50).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Получаем HTML-код страницы после загрузки всех комментариев
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Извлечение всех комментариев
        comments_user = soup.find_all("div", class_="comment__user")

        for comment in comments_user:
            username = comment.find("span", class_="user__nick")
            comments_list.append(username.get_text(strip=True))

# Закрываем драйвер
driver.quit()

# Удаляем дубликаты и записываем в файл
unique_comments = set(comments_list)

with open("only_nicks.txt", "a", encoding="utf-8") as file:
    for com in unique_comments:
        file.write(f"{com}\n")

print(unique_comments)
