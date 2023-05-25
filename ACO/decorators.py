import datetime


class EnterExitLog():
    def __init__(self, funcName):
        self.funcName = funcName

    def __enter__(self):
        print('Started: %s' % self.funcName)
        self.init_time = datetime.datetime.now()
        return self

    def __exit__(self, type, value, tb):
        print('Finished: %s in: %s seconds' % (self.funcName, datetime.datetime.now() - self.init_time))

def func_timer_decorator(func):
    def func_wrapper(*args, **kwargs):
        with EnterExitLog(func.__name__):
            return func(*args, **kwargs)

    return func_wrapper



def undefined_func_decorator(func):
    def wrapper(*args, **kwargs):
        raise ValueError(func.__name__ + " has not been implemented yet.")
    return wrapper