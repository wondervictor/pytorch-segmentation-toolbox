import os
import sys
import logging

# from . import pyt_utils
# from utils.pyt_utils import ensure_dir

_default_level_name = os.getenv('ENGINE_LOGGING_LEVEL', 'INFO')
_default_level = logging.getLevelName(_default_level_name.upper())


class LogFormatter(logging.Formatter):
    log_fout = None
    date_full = '[%(asctime)s %(lineno)d@%(filename)s:%(name)s] '
    date = '%(asctime)s '
    msg = '%(message)s'

    def format(self, record):
        if record.levelno == logging.DEBUG:
            mcl, mtxt = self._color_dbg, 'DBG'
        elif record.levelno == logging.WARNING:
            mcl, mtxt = self._color_warn, 'WRN'
        elif record.levelno == logging.ERROR:
            mcl, mtxt = self._color_err, 'ERR'
        else:
            mcl, mtxt = self._color_normal, ''

        if mtxt:
            mtxt += ' '

        if self.log_fout:
            self.__set_fmt(self.date_full + mtxt + self.msg)
            formatted = super(LogFormatter, self).format(record)
            # self.log_fout.write(formatted)
            # self.log_fout.write('\n')
            # self.log_fout.flush()
            return formatted

        self.__set_fmt(self._color_date(self.date) + mcl(mtxt + self.msg))
        formatted = super(LogFormatter, self).format(record)

        return formatted

    if sys.version_info.major < 3:
        def __set_fmt(self, fmt):
            self._fmt = fmt
    else:
        def __set_fmt(self, fmt):
            self._style._fmt = fmt

    @staticmethod
    def _color_dbg(msg):
        return '\x1b[36m{}\x1b[0m'.format(msg)

    @staticmethod
    def _color_warn(msg):
        return '\x1b[1;31m{}\x1b[0m'.format(msg)

    @staticmethod
    def _color_err(msg):
        return '\x1b[1;4;31m{}\x1b[0m'.format(msg)

    @staticmethod
    def _color_omitted(msg):
        return '\x1b[35m{}\x1b[0m'.format(msg)

    @staticmethod
    def _color_normal(msg):
        return msg

    @staticmethod
    def _color_date(msg):
        return '\x1b[32m{}\x1b[0m'.format(msg)


def get_logger(log_dir=None, log_file=None, formatter=LogFormatter):
    logger = logging.getLogger()
    logger.setLevel(_default_level)
    del logger.handlers[:]

    if log_dir and log_file:
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        LogFormatter.log_fout = True
        file_handler = logging.FileHandler(log_file, mode='a')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter(datefmt='%d %H:%M:%S'))
    stream_handler.setLevel(0)
    logger.addHandler(stream_handler)
    return logger


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.initialized = False
        self.val = None
        self.avg = None
        self.sum = None
        self.count = None

    def initialize(self, val, weight):
        self.val = val
        self.avg = val
        self.sum = val * weight
        self.count = weight
        self.initialized = True

    def update(self, val, weight=1):
        if not self.initialized:
            self.initialize(val, weight)
        else:
            self.add(val, weight)

    def add(self, val, weight):
        self.val = val
        self.sum += val * weight
        self.count += weight
        self.avg = self.sum / self.count

    def value(self):
        return self.val

    def average(self):
        return self.avg
    