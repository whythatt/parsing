import asyncio
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup


def fetch_comments(link):
    driver = webdriver.Chrome()  # Создаем новый экземпляр драйвера
    comments_list = []
    try:
        driver.get(link)

        # Ожидание загрузки страницы
        wait = WebDriverWait(driver, 30)
        wait.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Проверка наличия кнопки "Показать все комментарии"
        try:
            show_comments_button = wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "comment__more"))
            )
            # Если кнопка найдена, нажимаем на нее
            ActionChains(driver).move_to_element(show_comments_button).click().perform()
            print("Clicked on 'Show all comments' button.")
        except Exception:
            print("'Show all comments' button not found or not clickable.")

        # Ожидание подгрузки комментариев (если они загружаются динамически)
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "comment__user"))
        )

        # Получаем HTML-код страницы после загрузки всех комментариев
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")

        # Извлечение всех комментариев
        comments_user = soup.find_all("div", class_="comment__user")
        comments_list = [
            comment.find("span", class_="user__nick").get_text(strip=True)
            for comment in comments_user
            if comment.find("span", class_="user__nick")
        ]

    except Exception as e:
        print(f"Error fetching comments from {link}: {e}")
    finally:
        driver.quit()  # Закрываем драйвер

    return comments_list


async def main():
    comments_list = []

    with open("links_list.txt", "r", encoding="utf-8") as links_list:
        links = [link.strip() for link in links_list]  # Чтение и обрезка ссылок

        with ThreadPoolExecutor(max_workers=12) as executor:
            loop = asyncio.get_event_loop()
            tasks = [
                loop.run_in_executor(executor, fetch_comments, link) for link in links
            ]

            for result in await asyncio.gather(*tasks):
                comments_list.extend(result)

    # Удаление дубликатов и запись в файл
    unique_comments = set(comments_list)

    with open("only_nicks.txt", "a", encoding="utf-8") as file:
        file.write(
            "\n".join(unique_comments) + "\n"
        )  # Запись всех уникальных ников за раз

    print(unique_comments)


# Запуск асинхронного кода
if __name__ == "__main__":
    asyncio.run(main())
