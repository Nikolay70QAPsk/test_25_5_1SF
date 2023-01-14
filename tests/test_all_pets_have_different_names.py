import pytest

from settings import valid_email, valid_password
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')
    yield
    pytest.driver.quit()


@pytest.fixture()
def go_to_my_pets():
    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "email")))
    # Вводим email
    pytest.driver.find_element(By.ID, 'email').send_keys(valid_email)

    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    pytest.driver.find_element(By.ID, 'pass').send_keys(valid_password)

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
    # Нажимаем на ссылку "Мои питомцы"
    pytest.driver.find_element(By.LINK_TEXT, "Мои питомцы").click()


def test_all_pets_have_different_names(go_to_my_pets):
    """Поверяем что на странице со списком моих питомцев нет совпадающих имён"""

    WebDriverWait(pytest.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".table.table-hover tbody tr")))
    # Сохраняем в переменную pet_data элементы с данными о питомцах
    pet_data = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу. Выбираем имена и добавляем их в список pets_name.
    pets_name = []
    for i in range(len(pet_data)):
        data_pet = pet_data[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_name.append(split_data_pet[0])

    # Перебираем имена и если имя повторяется то прибавляем к счетчику r единицу.
    # Проверяем, если r == 0 то повторяющихся имен нет.
    r = 0
    for i in range(len(pets_name)):
        if pets_name.count(pets_name[i]) > 1:
            r += 1
    assert r == 0
    print(r)
    print(pets_name)
