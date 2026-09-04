import logging

_logger = None


def setup_logging(verbose=False):
    global _logger
    nivel = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=nivel,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )
    _logger = logging.getLogger("password_changer")
    return _logger


def get_logger():
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger
