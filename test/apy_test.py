import os
import allure
import requests
import pytest
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

api_key = os.getenv("X-API-KEY")
base_url_api = "https://api.poiskkino.dev/v1.4/"
main_headers = {"X-API-KEY": api_key}


@pytest.mark.api
@allure.id("Kinopoisk_api_01")
@allure.title("Поиск фильма по id. Позитивная проверка.")
@allure.severity("Critical")
def test_search_by_id():
    film_id = "45566"

    with allure.step("Отправка запроса."):
        response = requests.get(
            f"{base_url_api}movie/{film_id}",
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода."):
        assert (
            response.status_code == 200
        ), f"Ожидается статус 200, получен {response.status_code}"

    with allure.step("Парсинг JSON-ответа."):
        result = response.json()

    with allure.step("Проверка соответствия id."):
        assert str(result["id"]) == str(
            film_id
        ), (
            f"ID в ответе ({result.get('id')}) не совпадает "
            f"с запрошенным ({film_id})"
        )

    with allure.step("Проверка, что ответ не пустой."):
        assert len(result) > 0, "Ответ от API не должен быть пустым"


@pytest.mark.api
@allure.id("Kinopoisk_api_02")
@allure.title("Поиск фильма по названию. Позитивная проверка.")
@allure.severity("Critical")
def test_search_film_by_name():
    name_film = "1+1"

    with allure.step("Отправка запроса."):
        response = requests.get(
            url=f"{base_url_api}movie/search",
            params={"query": name_film},
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода."):
        assert (
            response.status_code == 200
        ), f"Ожидается статус 200, получен {response.status_code}"

    with allure.step("Парсинг JSON-ответа."):
        result = response.json()

    with allure.step("Проверка наличия списка фильмов."):
        assert "docs" in result, "В ответе отсутствует поле 'docs'"
        assert isinstance(
            result["docs"], list
        ), "Поле 'docs' должно быть списком"
        assert (
            len(result["docs"]) > 0
        ), "Список фильмов не должен быть пустым"

    with allure.step("Поиск фильма с нужным названием в ответе."):
        found = False
        for movie in result["docs"]:
            if "name" in movie and movie["name"].lower() == name_film.lower():
                found = True
                break
        assert found, (
            f"Фильм с названием '{name_film}' не найден "
            "в списке результатов"
        )


@pytest.mark.api
@allure.id("Kinopoisk_api_03")
@allure.title("Поиск актера по id. Позитивная проверка.")
@allure.severity("Critical")
def test_search_by_person_id():
    person_id = "1"

    with allure.step("Отправка запроса к API поиска актера по id."):
        response = requests.get(
            f"{base_url_api}person/{person_id}",
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода ответа."):
        assert (
            response.status_code == 200
        ), f"Ожидается статус 200, получен {response.status_code}"

    with allure.step("Парсинг JSON-ответа."):
        result = response.json()

    with allure.step("Проверка соответствия id актера в ответе."):
        assert str(result["id"]) == str(
            person_id
        ), (
            f"ID в ответе ({result.get('id')}) не совпадает "
            f"с запрошенным ({person_id})"
        )

    with allure.step("Проверка, что ответ не пустой."):
        assert len(result) > 0, "Ответ от API не должен быть пустым"


@pytest.mark.api
@allure.id("Kinopoisk_api_04")
@allure.title(
    "Поиск фильма по неверному токену авторизации. "
    "Негативная проверка."
)
@allure.severity("Normal")
def test_search_with_invalid_apiKey():
    movie_id = "100"
    invalid_key = {"X-API-KEY": "invalid_token_123"}

    with allure.step("Отправка запроса с неверным токеном авторизации."):
        response = requests.get(
            f"{base_url_api}movie/{movie_id}",
            headers=invalid_key,
        )

    with allure.step("Проверка статуса кода ответа."):
        assert (
            response.status_code == 401
        ), (
            f"При неверном токене ожидается статус 401, "
            f"получен {response.status_code}"
        )

    with allure.step(
        "Проверка, что в ответе есть признак ошибки авторизации."
    ):
        try:
            result = response.json()
            assert (
                "error" in result or "message" in result
            ), "В ответе должно быть сообщение об ошибке"
        except Exception:
            pass


@pytest.mark.api
@allure.id("Kinopoisk_api_05")
@allure.title(
    "Получение информации о фильме по неверному ID. "
    "Негативная проверка (статус 400)."
)
@allure.severity("Normal")
def test_search_by_invalid_id_bad_request():
    invalid_id = "0"

    with allure.step("Отправка запроса с заведомо неверным ID фильма."):
        response = requests.get(
            f"{base_url_api}movie/{invalid_id}",
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода ответа (ожидается 400)."):
        assert (
            response.status_code == 400
        ), (
            f"Ожидается статус 400 (Bad Request), "
            f"получен {response.status_code}"
        )

    with allure.step(
        "Проверка, что в ответе есть признак ошибки валидации ID."
    ):
        try:
            result = response.json()
            assert (
                "error" in result or "message" in result
            ), "В ответе должно быть сообщение об ошибке валидации ID"
        except Exception:
            pass


@pytest.mark.api
@allure.id("Kinopoisk_api_06")
@allure.title(
    "Поиск фильмов с недопустимым годом. "
    "Проверка 400 и сообщения об ошибке."
)
@allure.severity("Normal")
def test_search_by_invalid_year():
    invalid_year = "1110"
    url = f"{base_url_api.rstrip('/')}/movie"

    with allure.step("Отправка запроса с недопустимым годом выпуска."):
        response = requests.get(
            url,
            params={"year": invalid_year},
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода ответа (ожидается 400)."):
        assert (
            response.status_code == 400
        ), (
            f"Ожидается статус 400 (Bad Request), "
            f"получен {response.status_code}"
        )

    result = response.json()

    with allure.step("Проверка сообщения об ошибке валидации года."):
        messages = result.get("message", [])
        assert isinstance(messages, list), "Поле 'message' должно быть списком"
        assert any(
            "1874" in msg or "2050" in msg for msg in messages
        ), (
            f"В сообщении об ошибке должно быть упоминание "
            f"диапазона 1874–2050. Получено: {messages}"
        )

    with allure.step("Проверка поля error."):
        assert (
            result.get("error") == "Bad Request"
        ), f"Ожидается error='Bad Request', получено: {result.get('error')}"


@pytest.mark.api
@allure.id("Kinopoisk_api_07")
@allure.title(
    "Поиск фильмов с некорректным рейтингом IMDb "
    "(rating.imdb=-2-10). Негативная проверка (статус 400)."
)
@allure.severity("Normal")
def test_search_by_invalid_imdb_rating():
    invalid_rating = "-2-10"

    with allure.step("Отправка запроса с некорректным значением rating.imdb."):
        response = requests.get(
            f"{base_url_api}movie",
            params={"rating.imdb": invalid_rating},
            headers=main_headers,
        )

    with allure.step("Проверка статуса кода ответа (ожидается 400)."):
        assert (
            response.status_code == 400
        ), (
            f"Ожидается статус 400 (Bad Request), "
            f"получен {response.status_code}"
        )

    with allure.step(
        "Проверка, что в ответе есть признак ошибки валидации "
        "параметра rating.imdb."
    ):
        try:
            result = response.json()
            assert (
                "error" in result or "message" in result
            ), "В ответе должно быть сообщение об ошибке валидации рейтинга"
        except Exception:
            pass


@pytest.mark.api
@allure.id("Kinopoisk_api_08")
@allure.title("Некорректный запрос к эндпоинту person (статус 400).")
@allure.severity("Normal")
def test_incorrect_person_request():
    url = f"{base_url_api}person/"

    with allure.step(
        "Отправка запроса к эндпоинту person без обязательных параметров."
    ):
        response = requests.get(url, headers=main_headers)

    with allure.step("Проверка статуса кода ответа (ожидается 400)."):
        assert (
            response.status_code == 400
        ), (
            f"Ожидается статус 400 (Bad Request), "
            f"получен {response.status_code}"
        )

    with allure.step(
        "Проверка, что в ответе есть признак ошибки валидации запроса."
    ):
        try:
            result = response.json()
            assert (
                "error" in result or "message" in result
            ), "В ответе должно быть сообщение об ошибке валидации"
        except Exception:
            pass
