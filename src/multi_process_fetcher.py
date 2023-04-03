# GIL
import os
import sys
import threading
import time
from concurrent.futures.process import ProcessPoolExecutor

nums = [30] * 100

sys.set_int_max_str_digits(100000) # int 의 숫자 길이 확장

def cpu_bound_func(num):
    print(f"{os.getpid()} process | {threading.get_ident()} || {num}")
    numbers = range(1, num)
    total = 1
    for i in numbers:
        for j in numbers:
            for k in numbers:
                total *= i * j * k
    return total


def main():
    executor = ProcessPoolExecutor(max_workers=10)
    result = list(executor.map(cpu_bound_func, nums))
    print(result)


if __name__ == '__main__':
    start_time = time.time()
    main()
    end_time = time.time() - start_time
    print(end_time)
