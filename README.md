# Проект автоматизации тестирования API сайта учебного сервиса - Яндекс.Самокат

1. Основа для написания автотестов pytest, библиотека requests.
2. Применена Endpoints Component Model.
3. Подключен Allure-отчёт.
4. Установить зависимости — `pip install -r requirements.txt`
5. Команда для запуска тестов — `pytest -v`
6. Команда для запуска тестов с allure — `pytest`
7. Команда генерации статического отчета - `allure generate allure-results --clean -o my-report`
8. Команда для открытия отчета через сервер в браузере - `allure open my-report`