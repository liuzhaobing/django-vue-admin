# -*- coding:utf-8 -*-
import threading
import datetime
import concurrent.futures

CONTEXT_LOCK = threading.Lock()


class Context:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        with CONTEXT_LOCK:
            self.context = True

    def done(self):
        if self.context:
            return False
        return True

    def cancel(self):
        with CONTEXT_LOCK:
            if self.context:
                self.context = False


class WithTimeout(Context):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.expire_time = self.start_time + datetime.timedelta(*args, **kwargs)
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        self.executor.submit(self._timeout_counter)

    def __del__(self):
        self.executor.shutdown()

    def _timeout_counter(self):
        while True:
            if datetime.datetime.now() >= self.expire_time:
                if self.context:
                    return self.cancel()
