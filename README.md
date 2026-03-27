# Лабораторная работа № 2

---

## Описание 
В рамках второго спринта реализована доменная модель задачи (Task) с новыми полями и защитой инвариантов. В архитектуру внедрены data, non data дескрипторы и свойства (@property) для строгой валидации атрибутов (типы, диапазоны, переходы между статусами) и ленивых вычислений (суммарайз пэйлоада).

---

## Запуск проекта
Установка зависимостей
```bash
pip install -r requirements.txt
```

Запуск main.py (Демонстрации работы, не CLI)
```bash
python main.py
```
Логи будут сохраняться в logs.log (в корне проекта)

Запуск тестов с покрытием (92%)

```bash
pytest --cov=task_processor
```

---

## Структура проекта
```bash
lab
├── task_processor/
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── api_source.py
│   │   ├── file_source.py
│   │   └── generator_source.py
│   ├── __init__.py
│   ├── aggregator.py
│   ├── config.py
│   ├── descriptors.py
│   ├── exceptions.py
│   ├── protocol.py
│   └── task.py
├── tests/
├── logs.log
└── main.py
```
