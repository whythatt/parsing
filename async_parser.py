import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# Функция для инициализации драйвера и выполнения задач
def fetch_comments(link):
    driver = webdriver.Chrome()  # Создаем новый экземпляр драйвера для каждого потока
    try:
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
        comments_list = [
            comment.find("span", class_="user__nick").get_text(strip=True)
            for comment in comments_user
        ]

    finally:
        driver.quit()  # Закрываем драйвер

    return comments_list


async def main():
    # URL для загрузки постов
    url = "https://pikabu.ru/community/Bank/search?t=%D0%91%D0%B0%D0%BD%D0%BA&st=2"

    # Настройка драйвера для основной страницы
    driver = webdriver.Chrome()
    driver.get(url)

    # Прокрутка страницы вниз для подгрузки постов
    last_height = driver.execute_script("return document.body.scrollHeight")

    count_sleep = 0
    while True:
        print(count_sleep)
        count_sleep += 1
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Явное ожидание загрузки новых постов
        WebDriverWait(driver, 50).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        if count_sleep <= 15:
            time.sleep(5)
        time.sleep(3)
        print(count_sleep)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break  # Прокрутка завершена, если высота не изменилась

        last_height = new_height

    # Получаем HTML-код страницы после загрузки всех постов
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # Извлечение всех ссылок на комментарии
    comment_links = soup.find_all("a", class_="story__comments-link story__to-comments")
    links_list = [link["href"] for link in comment_links[:3]]

    driver.quit()  # Закрываем драйвер основной страницы

    # Параллельная обработка ссылок на комментарии с использованием ThreadPoolExecutor
    comments_list = []

    with ThreadPoolExecutor(
        max_workers=7
    ) as executor:  # Установите количество потоков по необходимости
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, fetch_comments, link) for link in links_list
        ]

        for result in await asyncio.gather(*tasks):
            comments_list.extend(result)

    # Удаляем дубликаты и записываем в файл
    unique_comments = set(comments_list)

    with open("only_nicks.txt", "a", encoding="utf-8") as file:
        for com in unique_comments:
            file.write(f"{com}\n")

    print(unique_comments)


# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())
