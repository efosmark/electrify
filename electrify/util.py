import time
import functools
import logging

from .value import format_value


class ContextTimer(object):

    def __init__(self, title, logger, logLevel=logging.DEBUG):
        self.title = title
        self.logger = logger
        self.logLevel = logLevel

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.stop = time.time()
        if self.logger.isEnabledFor(self.logLevel):
            self.logger.log(self.logLevel, 'CTX:{: <10}|{: ^10}'.format(
                self.title,
                format_value(self.stop - self.start, unit='s')
            ))

    def seconds(self):
        return time.time() - self.start


def logfunc(logger, logLevel=logging.DEBUG):
    def decorator_log(func):
        if not logger.isEnabledFor(logLevel):
            return func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            start = time.time()
            wrapped.num_calls += 1
            value = func(*args, **kwargs)
            runtime = time.time() - start
            full_arg_list = [
                *[str(a) for a in args],
                *['{}={}'.format(k, str(v)) for k, v in kwargs.items()]
            ]
            logger.log(logLevel, 'FUNC:{: <10}|{: ^3}|{: ^10}| ({}) = {}'.format(
                func.__name__,
                wrapped.num_calls,
                format_value(runtime, unit='s'),
                ", ".join(full_arg_list),
                str(value)
            ))
            return value
        wrapped.num_calls = 0
        return wrapped

    return decorator_log
