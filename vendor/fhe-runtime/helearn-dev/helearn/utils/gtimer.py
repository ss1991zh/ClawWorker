import time
from loguru import logger


class Timer(object):
    def __init__(self):
        self.inner_table = {}
        self.times = {}
        self.start_time = {}
        self.stop_time = {}

    def start(self, key):
        self.start_time[key] = time.time()
        self.stop_time[key] = None

    def stop(self, key):
        self.stop_time[key] = time.time()
        self.record(key, self.stop_time[key] - self.start_time[key])
        self.start_time[key] = None

    def record(self, key, val):
        if key not in self.inner_table:
            self.inner_table[key] = val
        else:
            self.inner_table[key] += val
        
        if key not in self.times:
            self.times[key] = 1
        else:
            self.times[key] += 1
    
    def summary(self):
        res = sorted(self.inner_table.items(), key=lambda x: x[1], reverse=True)
        for item in res:
            logger.info(f"{item[0]} \t总耗时: {item[1]* 1000:.2f}ms \t平均耗时[{self.times[item[0]]}次]:{item[1] / self.times[item[0]] * 1000:.2f} ms")


gt = Timer()
