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


def test_all_pets_are_present(go_to_my_pets):
    """Проверяем что на странице со списком моих питомцев присутствуют все питомцы"""

    # Сохраняем в переменную statistic элементы статистики
    statistic = pytest.driver.find_elements(By.CSS_SELECTOR, ".\\.col-sm-4.left")

    # Сохраняем в переменную pets элементы карточек питомцев
    pets = pytest.driver.find_elements(By.CSS_SELECTOR, '.table.table-hover tbody tr')

    # Получаем количество питомцев из данных статистики
    number = statistic[0].text.split('\n')
    number = number[1].split(' ')
    number = int(number[1])

    # Получаем количество карточек питомцев
    number_of_pets = len(pets)
    print('Количество моих питомцев:', number_of_pets)

    # Проверяем что количество питомцев из статистики совпадает с количеством карточек питомцев
    assert number == number_of_pets
