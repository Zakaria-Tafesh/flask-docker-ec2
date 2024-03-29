import datetime
import logging as logging
import traceback
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import os
from input.config import PATH_PARENT_PARENT


def create_log_dir(log_dir):
    print('Creating log directory: %s' % log_dir)
    try:
        os.makedirs(log_dir)
        print('Directory created successfully: %s' % log_dir)
    except FileExistsError:
        print(f'{log_dir} is already exists')
    except:
        traceback.print_exc()


def get_datetime_now():
    dt_now = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')
    return dt_now


PATH_THIS_FILE = os.path.realpath(__file__)

PATH_LOGS_DIR = os.path.join(PATH_PARENT_PARENT, 'logs')
PATH_LOGS_FILE = os.path.join(PATH_LOGS_DIR, 'script.log')

create_log_dir(PATH_LOGS_DIR)

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(u'%(asctime)s\t%(levelname)s\t%(filename)s:%(lineno)d\t%(message)s')


# create TimedRotatingFileHandler
# rotation_logging_handler = TimedRotatingFileHandler(PATH_LOGS,
#                                when='m',
#                                interval=1,
#                                backupCount=5)
# rotation_logging_handler.setLevel(logging.DEBUG)
# rotation_logging_handler.setFormatter(formatter)
# logger.addHandler(rotation_logging_handler)


# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


# Create a file handler
# fh = logging.FileHandler(PATH_LOGS)
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)
# logger.addHandler(fh)


# Create RotatingFileHandler
rfh = RotatingFileHandler(PATH_LOGS_FILE, maxBytes=1000_000, backupCount=5)
rfh.setLevel(logging.DEBUG)
rfh.setFormatter(formatter)
logger.addHandler(rfh)

