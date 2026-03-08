import logging
from pathlib import Path

def setup_logging():
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOG_FILE = BASE_DIR / 'logs.log'

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt='[ %(asctime)s ] %(name)s | %(levelname)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger = logging.getLogger('task_processor')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger


logger = setup_logging()
