from sys import  _getframe
from types import TracebackType
from functools import wraps
from threading import Lock
try:from openteab.main.lib.Exceptions import GetTypeName
except ImportError: from Exceptions import GetTypeName


def singleton(cls):
    '''
    trying to redefine a class will return the old one without args!
    '''
    instances = {}
    __lock = Lock()
    
    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in instances:
            with __lock:
                if cls not in instances: #DOUBLE CHECK AFTER LOCK
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton

def single(cls):
    '''
    ONLY ONE OF THIS CLASS CAN BE ALLOWED EVER!
    '''
    instances = {}
    __lock = Lock()
    @wraps(cls)
    def _singleton(*args, **kwargs):
        with __lock:
            if cls not in instances:
                    if cls not in instances: #DOUBLE CHECK AFTER LOCK
                        instances[cls] = cls(*args, **kwargs)
                        return instances[cls]
            else:
                previous_frame = _getframe(1)
                tb = TracebackType(tb_next=None,tb_frame=previous_frame,tb_lasti=previous_frame.f_lasti,tb_lineno=previous_frame.f_lineno)
                raise TypeError(f"CAN ONLY BE ONE INSTANCE OF {GetTypeName(cls)}").with_traceback(tb)
    return _singleton

class classproperty:
    '''
    ASSUMES it will be used at ANY LEVEL but will force STATIC LEVEL
    '''
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func()