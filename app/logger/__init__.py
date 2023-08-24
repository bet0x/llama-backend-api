import logging
import os
from logging import Logger


def suppress_loggers():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)


def __init__():
    print("Initializing logger with following configurations:", "Log file path: " + _get_log_file_path().__str__(),
          "Log level: " + logging.getLevelName(_get_log_level())
          , "Log format: " + _get_log_format().__str__())

    logging.basicConfig(
        filename=_get_log_file_path(),
        level=logging.ERROR,
        format=_get_log_format(),
    )

    suppress_loggers()
    print("Logger initialized.")


def get_logger(name: str) -> Logger:
    if name is None or name == "":
        name = "llama-backend"

    logger: Logger = logging.getLogger(name)
    logger.setLevel(_get_log_level())
    return logger


def _get_log_file_path() -> str:
    default_log_path = "logs/app.log"
    log_file_path = os.environ.get("LOG_FILE_PATH", default_log_path)

    if log_file_path is None or log_file_path == "":
        log_file_path = default_log_path

    if log_file_path is not None and not os.path.exists(log_file_path):
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    return log_file_path


def _get_log_level() -> str:
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    if log_level is not None and log_level != "":
        return logging.getLevelName(log_level)


def _get_log_format() -> str:
    default_log_format = "%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s"
    log_format = os.environ.get("LOG_FORMAT", default_log_format)

    if log_format is not None and log_format != "":
        return log_format

    return default_log_format

