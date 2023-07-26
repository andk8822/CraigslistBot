import os
import logging


log_directory = os.path.dirname(os.path.abspath(__file__))
debug_error_log_path = os.path.join(log_directory, 'debug_error.log')

# Логгер и обработчик для уровня INFO.
info_logger = logging.getLogger('info_logger')
info_logger.setLevel(logging.INFO)

info_handler = logging.StreamHandler()
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter('%(message)s')
info_handler.setFormatter(info_formatter)

info_logger.addHandler(info_handler)

# Логгер и обработчики для уровней DEBUG и ERROR.
debug_error_logger = logging.getLogger(__name__)
debug_error_logger.setLevel(logging.DEBUG)

debug_error_handler = logging.FileHandler(debug_error_log_path)
debug_error_handler.setLevel(logging.DEBUG)
debug_error_formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
debug_error_handler.setFormatter(debug_error_formatter)

debug_error_logger.addHandler(debug_error_handler)
