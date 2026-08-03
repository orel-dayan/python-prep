# import logging

# # Create a logger

# logger = logging.getLogger("SimpleLogger")
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(asctime)s   | %(levelname)s   | %(message)s')
# # Create a  StreamHandler to log to console 
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)

# file_handler = logging.FileHandler("errors.log")
# file_handler.setLevel(logging.ERROR)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")

# import logging

# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)

# file_handler = logging.FileHandler("app.log")
# file_handler.setLevel(logging.DEBUG)

# console_handler.setFormatter(
#     logging.Formatter("%(levelname)s: %(message)s")
# )

# file_handler.setFormatter(
#     logging.Formatter(
#         "%(asctime)s::%(levelname)s::%(name)s::%(funcName)s::%(lineno)d::%(message)s"
#     )
# )

# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# logger.debug("Debug message")
# logger.info("Application started")
# logger.warning("Low memory")
# logger.error("File not found")
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def fun(val):
    if val < 0:
        raise ValueError("Invalid value: Value cannot be negative.")
    else:
        logging.info("Operation performed successfully.")


try:
    v1 = int(input("Enter a value: "))
    fun(v1)
except ValueError as ve:
    logging.exception("Exception occurred: %s", str(ve))