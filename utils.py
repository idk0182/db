import time
from contextlib import contextmanager


@contextmanager
def measure_time():
    start = time.time()
    yield
    end = time.time()
    print(f"Время выполнения: {end - start:.4f} секунд")