import logging
import functools


logger = logging.getLogger(__name__)


def log_factory(level=logging.DEBUG):
    @functools.wraps(None)
    def deco(f):
        @functools.wraps(f)
        def wrapper(*arg, **kwargs):
            logger.log(level, f.__name__)
            return f(*arg, **kwargs)
        return wrapper
    return deco
