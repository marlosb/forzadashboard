import logging
from logging.handlers import RotatingFileHandler

def create_logger(name: str, 
                  log_level: int) -> logging.Logger:
    '''Creates a logger with the name provided and returns it'''
    logger = logging.getLogger(name.replace('_',''))
    logger.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    handler = RotatingFileHandler(f'logs/{name}.log', 
                                                   maxBytes=1024*1024, 
                                                   backupCount=5)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger