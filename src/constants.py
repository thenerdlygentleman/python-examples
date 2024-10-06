import logging

# NAMES
# ============================================================================ #
LOGFILE_NAME = "python-examples"
# ============================================================================ #


# Python logger
# ============================================================================ #
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
	"%(asctime)s | %(filename)s | [%(levelname)s] - %(message)s"
)

file_handler = logging.FileHandler(f"{LOGFILE_NAME}.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
# ============================================================================ #
