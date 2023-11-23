#多进程
from multiprocessing import Process

def func():
    for i in range(100000):
        print("sub",i)
    print("over!")

if __name__ == "__main__":
    p = Process(target=func)
    p.start()
    for j in range(100000):
        print("main",j)