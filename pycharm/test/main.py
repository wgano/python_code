from multiprocessing import Process

def sub():
    for i in range(1000):
        print("sub", i)


p = Process(target=sub)
p.start()
for j in range(1000):
    print("main", j)