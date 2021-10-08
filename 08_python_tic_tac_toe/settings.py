import logging

WINNERS_FILE = "winners.log"
WIN_COMBS = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7],
             [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

# file logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("winners_logger")
log_handler = logging.FileHandler(f"{WINNERS_FILE}", encoding='utf-8')
log_handler.setLevel(logging.DEBUG)
logger.addHandler(log_handler)