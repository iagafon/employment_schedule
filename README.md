# Employment Schedule
### Проект для проверки доступности временных слотов сотрудника на основе его рабочего графика.


# 📋 Описание

Сервис позволяет:

- Получать данные о рабочем графике сотрудника через API
- Проверять занятые и свободные промежутки времени
- Определять доступность конкретного временного слота
- Находить свободные окна для новых встреч

🛠 Установка

### 1. Убедитесь, что у вас установлены:
- Python 3.13+
- Poetry (менеджер зависимостей)

### 2. Клонируйте репозиторий:
`git clone https://github.com/iagafon/employment-schedule.git`

### 3. Установите зависимости:
`poetry install`

# 🚀 Использование
```
from src.check_slot_service.check_slot_service import CheckSlotService

if __name__ == "__main__":
    mock_date = "2025-02-15"
    mock_time_start = "15:00"
    mock_time_end = "16:40"

    CheckSlotService(mock_date, mock_time_start, mock_time_end)
```

# 🧪 Тестирование
`poetry run pytest`

# 📂 Структура проекта
```
src/
  check_slot_service/
    /dto                   # Pydantic модели
    __init__.py            # Инициализация пакета
    check_slot_service.py  # Основная логика
    main.py                # Точка входа
    schedule.py            # Работа с графиком
    time_slot.py           # Работа с временными промежутками
tests/
  check_slot_service/
    __init__.py
    conftest.py          # Фикстуры pytest
    test_*.py            # Тесты
```

# Justfile
### Установка зависимостей
```
install:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry install --no-root
```

### Запуск сервиса
```
run:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run python -m check_slot_service.main
```

### Запуск тестов
```
test:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run pytest
```

### Статическая проверка кода
```
lint:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run ruff check .
```

### Форматирование кода
```
format:
    source ./.venv/bin/activate && \
    export $(grep -v '^#' .env | xargs) && \
    poetry run ruff format .
```
