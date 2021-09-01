import selenium

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# time for pausing between navigation
import time
import itertools
import pandas as pd
import threading
import json
import sys

lock = threading.Lock()

results = []


def autotest(permutations_list, start, end):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option(
        "excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=chrome_options)

    # Open the website
    driver.get('https://pvpoke.com/team-builder/')

    setting = driver.find_element_by_class_name("arrow-down")
    setting.click()

    fill_team = Select(driver.find_element_by_class_name("quick-fill-select"))
    fill_team.select_by_index(2)

    time.sleep(2)

    for i in range(start, end):
        print(f"processing team #{i}")

        team_string = (
            permutations_list[i][0] + ' ' + permutations_list[i][1] + ' ' + permutations_list[i][2])

        add_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/button")))
        add_button.click()

        add_pokemon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[5]/div/div[3]/div/input")))
        add_pokemon.send_keys(permutations_list[i][0])

        add = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-poke")))
        add.click()

        add_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/button")))
        add_button.click()

        add_pokemon = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//div[5]/div/div[3]/div/input")))
        add_pokemon.send_keys(permutations_list[i][1])

        add = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-poke")))
        add.click()

        add_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[3]/div/div/div/button")))
        add_button.click()

        add_pokemon = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, "//div[5]/div/div[3]/div/input")))
        add_pokemon.send_keys(permutations_list[i][2])

        add = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".save-poke")))
        add.click()

        rate = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".rate-btn")))
        rate.click()

        coverage = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".coverage .grade"))).text
        bulk = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".bulk .grade"))).text
        safety = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".safety .grade"))).text
        consistency = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".consistency .grade"))).text
        threat_score = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".threat-score"))).text

        rating_string = (coverage + ' ' + bulk + ' ' +
                         safety + ' ' + consistency)

        with lock:
            results.append(
                {'team': team_string, 'rating': rating_string, 'score': threat_score})

        time.sleep(0.5)

        remove = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/div/a")))
        remove.click()

        confirm = WebDriverWait(driver, 5).until(EC.element_to_be_clickable(
            (By.XPATH, "/html/body/div[5]/div/div[3]/div/div/div[1]")))
        confirm.click()

    driver.quit()


if __name__ == "__main__":
    print(f"EXEC #{sys.argv[1]}")

    EXEC_TIME = int(sys.argv[1])

    permutations_list = json.load(open('permutations_list.json'))

    # cast back to tuples
    permutations_list = [tuple(pokemon) for pokemon in permutations_list[len(
        permutations_list)//100*EXEC_TIME:len(permutations_list)//100*(EXEC_TIME+1)]]

    # print(permutations_list)

    thread = 13
    threads = []

    for i in range(thread):
        t = threading.Thread(target=autotest, args=(
            permutations_list, (len(permutations_list)//thread)*i, (len(permutations_list)//thread)*(i+1),))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    look = sorted(results, key=lambda k: k["score"])
    print(look)

    f = open(f"result-{EXEC_TIME}.json", "w", encoding="utf-8")
    json.dump(look, f, ensure_ascii=False)
    f.close()
