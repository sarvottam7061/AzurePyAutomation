import logging


def get_logger():
    """
    Getter method to return the logger that writes the log messages in report

        Returns: logger

    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger
