import os
import logging
import inspect
import functools

from .spoc.etypes import SpoccerColumnException


def log(logger, level=logging.DEBUG):
    '''
    Signal execution of the annotated function in logs
    '''
    def deco(f):
        modulename = inspect.getmodule(f).__name__.split('.')[-1]
        msg = f'{modulename} - {f.__name__} - {{self}} - OK'

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            logger.log(level, msg.format(self=args[0]))
            return response
        return wrapper
    return deco


def catch(logger, exceptions=(SpoccerColumnException,)):
    '''
    Raise or catch exceptions in the annotated function
    '''
    def deco(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            # raise
            if bool(int(os.environ.get('RAISE', 1))):
                return f(*args, **kwargs)
            # catch
            try:
                return f(*args, **kwargs)
            except exceptions as e:
                modulename = inspect.getmodule(f).__name__.split('.')[-1]
                logger.error(f'{modulename} - {f.__name__} - {e}')
        return wrapper
    return deco
