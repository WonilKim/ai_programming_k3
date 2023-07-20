from multiprocessing import Pool
import time

def work(x):
    print(x)


if __name__ == "__main__":
    pool = Pool(10)
    data = range(1, 1000)
    t0 = time.time_ns()
    pool.map(work, data)
    t1 = time.time_ns()

    print("Time:{}".format(t1 - t0))

