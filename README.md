# Лабораторная работа № 3

---

## Описание 
В рамках третьей лабораторной работы реализована очередь задач (TaskQueue), поддерживающая итерацию, повторный обход и ленивую фильтрацию. Использование генераторов обеспечивает эффективную работу с большими объемами данных без избыточного хранения в памяти. Очередь совместима со стандартными конструкциями Python (for, list, sum).

---

## Запуск проекта
Установка зависимостей
```bash
pip install -r requirements.txt
```

Запуск main.py (Демонстрация работы)
```bash
python main.py
```
Логи будут сохраняться в logs.log (в корне проекта)

Запуск тестов с покрытием

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
│   ├── queue.py
│   └── task.py
├── tests/
│   ├── __init__.py
│   ├── test_aggregator.py
│   ├── test_api_source.py
│   ├── test_descriptors.py
│   ├── test_file_source.py
│   ├── test_generator_source.py
│   ├── test_queue.py
│   └── test_task.py
├── logs.log
├── main.py
├── README.md
└── requirements.txt
```
