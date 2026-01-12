### Запуск сервера

1. Установите Poetry 
pip install poetry
2. Войдите в виртуальное окружение
poetry shell
3. Установите зависимости
poetry install
4. Клонируйте репозиторий git clone git@github.com:rustamgabdelislamov/home_work_30.git
5. Сгенерируй SSH ключ и загрузи его в SSH keys , также сгенерируй SSH ключ для nginx на сервере
ssh-keygen -t ed25519 -C "your@email"
6. Создайте в секретах  на GIT HUB 
DEPLOY_DIR
DOCKER_HUB_ACCESS_TOKEN
DOCKER_HUB_USERNAME
SECRET_KEY
SERVER_IP
SSH_KEY
SSH_USER
7.Сделайте commit и push в репозиторий и сервер развернется сам


