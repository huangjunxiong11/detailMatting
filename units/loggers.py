# coding:utf-8
"""
通用logger
"""
import functools
import logging
import traceback
import uuid
from logging.handlers import RotatingFileHandler


class _LogLevelFilter(logging.Filter):

    def __init__(self, name='', level=logging.DEBUG):
        super(_LogLevelFilter, self).__init__(name)
        self.level = level

    def filter(self, record):
        return record.levelno == self.level


class MyException(Exception):
    pass


class EasyLoggers:

    def __init__(self, file_path=None, mode='w', silent=False, setlevel='debug', formatter=None, rotate=False,
                 maxsize=50, maxcount=10):

        self.mode = mode
        self.file_path = file_path
        self.silent = silent
        self.setlevel = setlevel
        self.formatter = formatter
        self.rotate = rotate
        self.maxsize = maxsize
        self.maxcount = maxcount

        self.console = None
        self.fileHandler = None
        self.rthandler = None
        self.loggers = logging.getLogger(str(uuid.uuid1()).replace('-', ''))
        if self.formatter is None:
            fmt = '[%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s] :: %(message)s'
            self.formatter = logging.Formatter(fmt)

    @property
    def log_print(self):
        """
        normal logging
        """

        __level = {'debug': logging.DEBUG,
                   'info': logging.INFO,
                   'warning': logging.WARNING,
                   'critical': logging.CRITICAL,
                   'error': logging.ERROR}

        self.loggers.setLevel(__level[self.setlevel])
        filters = _LogLevelFilter(level=__level[self.setlevel])

        # 存在句柄时，控制窗只需出现一个
        if not self.loggers.handlers:
            if self.silent is False and self.console is None:
                self.console = logging.StreamHandler()
                self.console.setFormatter(self.formatter)
                self.loggers.addHandler(self.console)

        if self.file_path is not None and self.rotate is False and self.fileHandler is None:
            self.fileHandler = logging.FileHandler(self.file_path, mode=self.mode, encoding='utf8')
            self.fileHandler.setFormatter(self.formatter)
            # file.addFilter(filters)
            self.loggers.addHandler(self.fileHandler)

        if self.file_path is not None and self.rotate is True and self.rthandler is None:
            self.rthandler = RotatingFileHandler(self.file_path,
                                                 maxBytes=self.maxsize * 1024 * 1024,
                                                 backupCount=self.maxcount)
            self.rthandler.setFormatter(self.formatter)
            # Rthandler.addFilter(filters)
            self.loggers.addHandler(self.rthandler)

        return self.loggers

    @property
    def log_error(self):
        """
        loggging @
        """

        def _exception(function):
            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                err = ''
                try:
                    return function(*args, **kwargs)
                except:
                    err += '\n' + traceback.format_exc()
                    self.log_print.error(err)
                finally:
                    if err != '':
                        raise MyException(err)

            return wrapper

        return _exception
