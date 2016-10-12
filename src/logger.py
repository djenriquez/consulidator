import logging
import os

def initialize_logger():
    log_level = getattr(logging, os.getenv('LOG_LEVEL', default='WARNING').upper(), None)
    logging.basicConfig(level=log_level, format='%(levelname)s:%(name)s:%(asctime)s %(message)s')