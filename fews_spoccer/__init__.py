import logging


def add_loghandler(logger, handler, loglevel, formatter, **kwargs):
    '''
    Add loghandler, kwargs are passed to handler instance
    '''
    handler = handler(**kwargs)
    handler.setLevel(loglevel)
    handler.setFormatter(formatter)
    logger.addHandler(handler)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fmt_file = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')
fmt_stream = logging.Formatter(
    '%(levelname)s - %(module)s - %(funcName)s - %(message)s')

add_loghandler(
    logger, logging.FileHandler, logging.DEBUG, fmt_file,
    filename='./log.log', mode='w')
add_loghandler(
    logger, logging.StreamHandler, logging.INFO, fmt_stream)

logger.debug('Base logger initialized')
