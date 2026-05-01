# Лабораторная работа № 4

---

## Описание
В рамках лабораторной работы добавлен асинхронный исполнитель задач. Система сохраняет архитектуру прошлых лабораторных работ: задачи собираются из источников, попадают в очередь, после чего обрабатываются асинхронными воркерами через расширяемые обработчики

Реализованы:
- асинхронная очередь задач AsyncTaskQueue на базе asyncio.Queue
- контракт обработчика TaskHandler через typing.Protocol
- AsyncTaskExecutor с асинхронным контекстным менедджером
- централизованное логирование ошибок обработки
- неблокирующий DefaultTaskHandler для демонстрации async/await

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

Покрытие составляет 92%

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
│   ├── async_queue.py
│   ├── config.py
│   ├── descriptors.py
│   ├── exceptions.py
│   ├── executor.py
│   ├── handlers.py
│   ├── protocol.py
│   ├── queue.py
│   └── task.py
├── tests/
├── logs.log
├── main.py
├── README.md
└── requirements.txt
```
