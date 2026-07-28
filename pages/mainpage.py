from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import WebDriver

# создание класса
class MainPage:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    SEARCH='//input[@placeholder="Фильмы, сериалы, персоны"]'
    TOP="//section[.//h2[contains(text(),'Возможно, вы искали')]]//span[text()='Мачеха']"

    selector = ('[class="film-poster styles_root__J_gIg '
                'styles_rootInLight__iqWuw image styles_root__95qkI"]'
                )

    def open_main_page(self, url: str = "https://www.kinopoisk.ru/") -> WebDriver:
        """открыть главную страницу"""
        self.driver.get(url)
        return self.driver

        """ввод фразы в строке поиска"""

    def search_by_phrase(self, phrase: str):
        search_input = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, self.SEARCH)))
        search_input.clear()
        search_input.send_keys(phrase)
        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

        """получение результатов поиска"""

    def get_search_results(self) -> list:
        results_selector = 'js-serp-metrik'
        results = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, results_selector))
        )
        return results

    def get_top_search_results(self, name: str):
        """возвращает название фильма, первого в поиске"""
        result = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//section[.//h2[contains(text(),'Возможно, вы искали')]]//span[text()='{name}']"
                 )
            )
        )
        return result.text

    # переход по разделу меню Билеты в кино
    def go_to_movie_tickets(self):
        """Метод для перехода на вкладку «Билеты в кино» на Кинопоиске"""

        # Поиск по тексту ссылки
        tickets_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Билеты в кино')]")
            )
        )
        tickets_link.click()
        return self.driver.title

    # поиск отображение элемента по селектору (CSS)

    def search_CSS_selector(self):
        element = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, self.selector))
        )
        return element

        # переход к разделу меню Фильмы

    def go_to_movie_films(self):
        """Метод для перехода на вкладку «Фильмы» на Кинопоиске"""

        # Поиск по тексту ссылки
        films_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[@href="/lists/categories/movies/1/"]')
            )
        )

        films_link.click()
        return self.driver.title

    # проверка заголовка главной страницы

    def go_to_serial(self):
        """Метод для перехода на вкладку «Сериалы» на Кинопоиске"""

        #  # переход к разделу меню Сериалы
        serial_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[@href="/lists/categories/movies/3/"]')
            )
        )

        serial_link.click()
        return self.driver.title

