import logging

# Создание объекта логгера
logger = logging.getLogger(__name__)

# Установка уровня логирования (можно изменить по своему усмотрению)
logger.setLevel(logging.DEBUG)

# Создание обработчика, который будет записывать логи в файл
log_file = "application.log"
file_handler = logging.FileHandler(log_file)

# Установка уровня логирования для обработчика (можно изменить по своему усмотрению)
file_handler.setLevel(logging.DEBUG)

# Создание форматтера для сообщений лога
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

# Привязка форматтера к обработчику
file_handler.setFormatter(formatter)

# Добавление обработчика в логгер
logger.addHandler(file_handler)
