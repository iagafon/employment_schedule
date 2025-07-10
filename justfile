# Установка зависимостей
install:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry install --no-root

# Запуск сервиса
run:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run python -m check_slot_service.main

# Запуск тестов
test:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run pytest

# Статическая проверка кода
lint:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run ruff check .

# Форматирование кода
format:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run ruff format .
