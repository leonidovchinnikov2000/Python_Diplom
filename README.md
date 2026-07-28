### Дипломный проект по Автоматизации UI- и API финального проекта  по ручному тестированию
 [ссылка на проект](https://ovchinnikovla-qa118.yonote.ru/share/493764dd-d2f5-4d63-828a-b5a6849d2568)
## Шаги работы
 1. Склонировать проект 'git clone https://github.com/leonidovchinnikov2000/Python_Diplom.git
 2. Установить зависимости
 3. Запустить тесты 
## Команды для запуска тестов
Все тесты (UI + API):
bash
pytest 

Только API тесты
bash
pytest -m api -v

Только UI тесты
bash
pytest -m ui -v

Запуск с Allure отчетом
bash
pytest --alluredir=allure-results -v
allure serve allure-results

Запуск конкретного тестового файла
bash
pytest tests/apy_test.py -v
pytest tests/ui_test.py -v


## Стек:
-selenium,
-requests,
-pytest,
-allure.
 
## Настройка переменных окружения
Создание файла .env и заполнить необходимые значения:
    X_API_KEY="ВАШ КЛЮЧ"

## Библиотеки 
- pip install requests
