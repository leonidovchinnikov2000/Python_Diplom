import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    """Фикстура для создания браузера."""
    driver_obj = webdriver.Chrome()
    driver_obj.maximize_window()
    yield driver_obj
    driver_obj.quit()
