import inspect
import random
import time
import functools
import logging
from collections import defaultdict
from uuid import uuid4
from base64 import standard_b64encode
from typing import Any, Callable, ClassVar, Dict, Generator, List, Optional, TypeVar

from .value import format_value

def short_uid(maxlen=8) -> str:
    b64 = standard_b64encode(uuid4().bytes)
    uid_chrs = [chr(b) for b in b64 if chr(b) not in ('=', '/', '+')][:maxlen]
    uid_chrs[random.randint(1, len(uid_chrs)-2)] = ' '
    return "".join(uid_chrs)

def ellipsis(content:str, max_length:int=0) -> str:
    if max_length > 0 and max_length < len(content)-1:
        return content[:max_length-1] + '…'
    return content

def get_func_info(func, *args, **kwargs) -> tuple[str, list[tuple[str, Any]]]:
    func_name = func.__name__
    arg_names = get_arg_names(func)
    arg_values = [*args]
    
    if arg_names[0] in ('self', 'cls'):
        arg_names = arg_names[1:]
        arg_values = arg_values[1:]
        func_name = f"{args[0].__class__.__name__}.{func_name}"
    
    if func.__name__ in ('__init__', '__new__'):
        func_name = args[0].__class__.__name__

    arg_names.extend(kwargs.keys())
    arg_values.extend(kwargs.values())
    return func_name, list(zip(arg_names, arg_values))


INDENT = '│  '
COMPACT_INDENT = '│'

class ContextTimer:
    def __init__(self, name:str, on_complete:Optional[Callable]=None):
        self.name = name
        self.on_complete = on_complete
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.stop = time.time()
        if self.on_complete is not None:
            self.on_complete(self)
    
    def duration(self) -> float:
        return (time.time() if self.stop is None else self.stop) - self.start

class StackLogger:
    _stack_depth:ClassVar[int] = -1
    _counters:Dict[str, int]
    
    def __init__(self, logger:Optional[logging.Logger]=None, log_level:Optional[int]=None, compact=False):
        if logger is None:
            logger = logging.getLogger(self.__class__.__name__)
            logger.setLevel(logging.DEBUG)
        if log_level is None:
            log_level = logging.DEBUG
        self.logger = logger
        self.log_level = log_level
        self.compact = compact
        self._counters = defaultdict(int)
        self._previous_line_empty = False

    def log_counters(self):
        self.log(" ")
        self.log("| Count | %s |", "Name".ljust(50))
        self.log("| ----- | " + ("-" * 50) + ' |')
        for name, count in sorted(self._counters.items(), key=lambda x:x[1], reverse=True):
            self.log('| %05s | %s |', format_value(count), name.ljust(50))
        self.log(" ")
    
    def log(self, m:str='', *args):
        if self._previous_line_empty and m == '':
            return
        self.logger.log(
            self.log_level,
            '{}{}'.format(
                (COMPACT_INDENT if self.compact else INDENT) * self._stack_depth,
                m
            ),
            *args
        )
        self._previous_line_empty = (m == '')
    
    def timed(self, name:str):
        StackLogger._stack_depth += 1
        if not self.compact:
            self.log()
        self.count(f'TIMER:{name}')
        self.log('┌[TIMER "{}"]'.format(name))
        return ContextTimer(name, self._on_timed_completed)
    
    def _on_timed_completed(self, timer:ContextTimer):
        self.log('└[TIMER "{}"] {}S'.format(
            timer.name,
            format_value(timer.duration())
        ))
        if not self.compact:
            self.log()
        StackLogger._stack_depth -= 1
    
    def message(self, message:str, *args):
        self.log(f'│ {message}', *args)
    
    def count(self, name):
        self._counters[name] += 1
    
    def func(self, func:Callable):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            
            if not self.logger.isEnabledFor(self.log_level):
                return func(*args, **kwargs)
            
            StackLogger._stack_depth += 1
            func_name, arg_list = get_func_info(func, *args, **kwargs)
            self.count(f'FUNC:{func_name}')
            
            if not self.compact:
                self.log()
            self.log('┌{}({})'.format(
                func_name,
                ", ".join([
                    f'{k}={repr(ellipsis(str(v), 50))}'
                    for k, v in arg_list
                ])
            ))
            
            value = func(*args, **kwargs)
            self.log('└{}'.format(value))
            if not self.compact:
                self.log()
            StackLogger._stack_depth -= 1
            return value
    
        return wrapped















def logfunc(logger, log_level=logging.DEBUG):
    def decorator_log(func):
        if not logger.isEnabledFor(log_level):
            return func

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            func_name = func.__name__
            arg_names = get_arg_names(func)
            arg_values = [*args]
            
            if arg_names[0] in ('self', 'cls'):
                arg_names = arg_names[1:]
                arg_values = arg_values[1:]
                func_name = f"{args[0].__class__.__name__}.{func_name}"
            
            if func.__name__ in ('__init__', '__new__'):
                func_name = args[0].__class__.__name__
            
            full_arg_list = [
                *[repr(a) for i,a in enumerate(arg_values)],
                *[f'{k}={repr(ellipsis(str(v), 20))}' for k, v in kwargs.items()]
            ]
            
            
            start = time.time()
            value = func(*args, **kwargs)
            runtime = time.time() - start
            
            logger.log(log_level, '{}({}) = {}'.format(
                func_name,
                ", ".join(full_arg_list),
                repr(value)
            ))
            return value
        
        return wrapped    
    return decorator_log



_V = TypeVar("_V")
def visit_once(sequence:List[_V], as_stack=False) -> Generator[_V, _V, Any]:
    seen = set()
    while len(sequence) > 0:
        item = sequence.pop() if as_stack else sequence.pop(0)
        if item not in seen and item is not None:
            seen.add(item)
            yield item


def get_arg_names(func: Callable) -> list[str]:
    argspec = inspect.getfullargspec(func)
    args = argspec[0]
    defaults = argspec[3]
    if defaults is not None and len(defaults) > 0:
        return args[0:0 - len(defaults)]
    return args
