import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# URL для загрузки постов
url = "https://pikabu.ru/community/Bank/search?t=%D0%91%D0%B0%D0%BD%D0%BA&st=2"
#
# # Настройка драйвера для основной страницы
driver = webdriver.Chrome()
driver.get(url)

# Прокрутка страницы вниз для подгрузки постов
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Явное ожидание загрузки новых постов
    WebDriverWait(driver, 5000).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # time.sleep(9)
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".story"))
    )

    new_height = driver.execute_script("return document.body.scrollHeight")

    if new_height == last_height:
        break  # Прокрутка завершена, если высота не изменилась

    last_height = new_height

# Получаем HTML-код страницы после загрузки всех постов
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")

# Извлечение всех ссылок на комментарии
comment_links = soup.find_all("a", class_="story__comments-link story__to-comments")
links_list = [link["href"] for link in comment_links]
print(len(links_list))
links_list = set(links_list)

# with open("links_list.txt", "a", encoding="utf-8") as file:
#     for li in links_list:
#         file.write(f"{li}\n")

driver.quit()  # Закрываем драйвер основной страницы
