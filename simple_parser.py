import asyncio
import time
from concurrent.futures import ThreadPoolExecutor

import lxml
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

comments_list = []


def get_comments(link):
    driver = webdriver.Chrome()
    driver.get(link)

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".comment__user"))
    )
    try:
        comment_more = driver.find_element(By.CSS_SELECTOR, ".comment__more")
        ActionChains(driver).move_to_element(comment_more).click().perform()
        comment_more = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".comment__more"))
        )
        comment_more.click()
        print(f"i am click on the button - {link}")
    except Exception:
        print(f"not button - {link}")

    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "comment__user"))
    )

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "lxml")
    driver.quit()

    # Извлечение всех комментариев
    comments_user = soup.find_all("div", class_="comment__user")
    with open("simple_only_niks.txt", "a", encoding="utf-8") as file:
        for com in comments_user:
            comment = com.find("span", class_="user__nick").get_text(strip=True)
            comments_list.append(comment)
            file.write(f"{comment}\n")


links = [
    "https://pikabu.ru/story/idealnyiy_kredit_11967968#comments",
    "https://pikabu.ru/story/tretiy_poshel_9647386#comments",
    "https://pikabu.ru/story/prodolzhenie_posta_banki_vyistupili_protiv_novogo_zakona_o_shtrafakh_za_utechki_dannyikh_11119789#comments",
    "https://pikabu.ru/story/razvod_banka_ili_ya_loshara_5871019#comments",
    "https://pikabu.ru/story/banki_takie_banki_7459954#comments",
    "https://pikabu.ru/story/otvet_na_post_igra_v_tinkoff_sotrudniki_i_rukovodstvo_9386555#comments",
]
with ThreadPoolExecutor(max_workers=3) as executor:
    executor.map(get_comments, links)

print(comments_list)
