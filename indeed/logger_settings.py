import logging


# Создать логгер.
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создать обработчик для уровня DEBUG, задать его формат.
debug_handler = logging.FileHandler('debug.log', mode='w')
debug_handler.setLevel(logging.ERROR)
debug_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
debug_handler.setFormatter(debug_formatter)

# Создать обработчик для уровня INFO, задать его формат.
info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(message)s')
info_handler.setFormatter(info_formatter)

# Создать обработчик для уровня ERROR, задать его формат.
error_handler = logging.FileHandler('error.log', mode='w')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
error_handler.setFormatter(error_formatter)

# Добавить обработчики в логгер.
logger.addHandler(debug_handler)
logger.addHandler(info_handler)
logger.addHandler(error_handler)
