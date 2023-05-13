from time import time

class Profiler:
    class Logger:
        def __init__(self):
            self._lock = False
            self._logs = []

        def start(self):
            assert not self._lock, 'Locked'
            self._lock = True
            self._tic = time()

        def stop(self, toc):
            assert self._lock, 'Unlocked'
            self._logs.append(toc - self._tic)
            self._lock = False

        def get(self):
            return self._logs

    _key_to_logger = dict()
    _key_stack = []

    @classmethod
    def __init__(cls, key):
        if key not in cls._key_to_logger.keys():
            cls._key_to_logger[key] = cls.Logger()
        cls._key_stack.append(key)

    @classmethod
    def __enter__(cls):
        cls._key_to_logger[cls._key_stack[-1]].start()

    @classmethod
    def __exit__(cls, *exc):
        toc = time()
        cls._key_to_logger[cls._key_stack.pop()].stop(toc)

    @classmethod
    def start_range(cls, key):
        if key not in cls._key_to_logger.keys():
            cls._key_to_logger[key] = cls.Logger()
        cls._key_to_logger[key].start()

    @classmethod
    def stop_range(cls, key):
        toc = time()
        cls._key_to_logger[key].stop(toc)

    @classmethod
    def get_logs(cls, key=None):
        # Return raw logs.
        #
        # Parameters
        # ----------
        # key: task identifier. Default returns logs of all tasks.
        # ----------

        if key is None:
            items = [(key, logger.get()) for key, logger in cls._key_to_logger.items()]
        else:
            assert key in cls._key_to_logger.keys(), 'Invaild key'
            items = [(key, cls._key_to_logger[key].get())]
        return items

    @classmethod
    def summary(cls, process=None, key=None):
        # Return summerized logs as JSON formatted ``str``.
        #
        # Parameters
        # ----------
        # process: process identifier. Default returns logs without identifier.
        # key: task identifier. Default returns logs of all tasks.
        # ----------

        from json import dumps
        if process is None:
            output = {'data': {}}
        else:
            output = {'process': process, 'data': {}}

        for key, log in cls.get_logs(key):
            if len(log):
                value = {'count': len(log), 'accu': sum(log), 'min': min(log), \
                                    'max': max(log), 'mean': sum(log) / len(log)}
                output['data'][key] = value
            else:
                output['data'][key] = {}
        return dumps(output)

    @classmethod
    def clear(cls):
        cls._key_to_logger = dict()
        cls._key_stack = list()
