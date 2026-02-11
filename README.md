### Запуск сервера

1. Установите Poetry 
pip install poetry
2. Войдите в виртуальное окружение
poetry shell
3. Установите зависимости
poetry install
4. Клонируйте репозиторий git@github.com:rustamgabdelislamov/Number_auth.git
5. Выполните команды
python manage.py csu
python manage.py add_user
6. Запустите Docker Desktop
5. Соберите контейнер 
docker-compose up -d
6. Войдите в браузер http://127.0.0.1:8000/ и подтверждайте свой номер
7. Для Postmana есть коллекция в которой все запросы подписаны и есть тело запросов


