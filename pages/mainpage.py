import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver


class MainPage:
    SEARCH = '//input[@placeholder="Фильмы, сериалы, персоны"]'
    TOP = (
        "//section[.//h2[contains(text(),'Возможно, вы искали')]]"
        "//span[text()='Мачеха']"
    )

    selector = (
        '[class="film-poster styles_root__J_gIg '
        'styles_rootInLight__iqWuw image styles_root__95qkI"]'
    )

    def __init__(self, driver: WebDriver, url: str) -> None:
        self.driver = driver
        self.url = url
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть главную страницу")
    def open_main_page(
        self,
        url: str = "https://www.kinopoisk.ru/"
    ) -> WebDriver:
        """Открыть главную страницу."""
        self.driver.get(url)
        return self.driver

    @allure.step("Ввод фразы в строке поиска")
    def search_by_phrase(self, phrase: str) -> None:
        """Ввод фразы в строке поиска и отправка запроса."""
        search_input = self.wait.until(
            EC.presence_of_element_located((By.XPATH, self.SEARCH))
        )
        search_input.clear()
        search_input.send_keys(phrase)
        self.driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

    @allure.step("Получение результатов поиска")
    def get_search_results(self) -> list:
        """Получить список элементов результатов поиска."""
        results_selector = "js-serp-metrik"
        results = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, results_selector)
            )
        )
        return results

    @allure.step("Получить топ-результат поиска по названию")
    def get_top_search_results(self, name: str) -> str:
        """Возвращает название фильма, первого в подсказке
        «Возможно, вы искали»."""
        locator = (
            f"//section[.//h2[contains(text(),'Возможно, вы искали')]]"
            f"//span[text()='{name}']"
        )
        result = self.wait.until(
            EC.presence_of_element_located((By.XPATH, locator))
        )
        return result.text

    @allure.step("Переход на вкладку «Билеты в кино»")
    def go_to_movie_tickets(self) -> str:
        """Метод для перехода на вкладку «Билеты в кино» на Кинопоиске."""
        tickets_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[contains(text(), 'Билеты в кино')]")
            )
        )
        tickets_link.click()
        return self.driver.title

    @allure.step("Поиск элемента по сложному CSS-селектору")
    def search_css_selector(self):
        """Поиск отображения элемента по селектору (CSS)."""
        element = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, self.selector))
        )
        return element

    @allure.step("Переход на вкладку «Фильмы»")
    def go_to_movie_films(self) -> str:
        """Метод для перехода на вкладку «Фильмы» на Кинопоиске."""
        films_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[@href="/lists/categories/movies/1/"]')
            )
        )
        films_link.click()
        return self.driver.title

    @allure.step("Переход на вкладку «Сериалы»")
    def go_to_serial(self) -> str:
        """Метод для перехода на вкладку «Сериалы» на Кинопоиске."""
        serial_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//a[@href="/lists/categories/movies/3/"]')
            )
        )
        serial_link.click()
        return self.driver.title
