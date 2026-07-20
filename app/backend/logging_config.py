import logging
import sys

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RED = "\033[31m"

LEVEL_COLORS = {
    logging.DEBUG: DIM,
    logging.INFO: GREEN,
    logging.WARNING: YELLOW,
    logging.ERROR: RED,
}


class DidacticFormatter(logging.Formatter):
    def format(self, record):
        color = LEVEL_COLORS.get(record.levelno, RESET)
        prefix = f"{color}{BOLD}[{record.name}]{RESET}"
        return f"{prefix} {record.getMessage()}"


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(DidacticFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(logging.INFO)

    logging.getLogger("uvicorn.access").handlers = [handler]


def get_logger(name):
    return logging.getLogger(name)


def section(title, color=CYAN):
    line = "─" * (len(title) + 4)
    print(f"{color}┌{line}┐{RESET}")
    print(f"{color}│  {BOLD}{title}{RESET}{color}  │{RESET}")
    print(f"{color}└{line}┘{RESET}")
