def add(n):
    return 1/(pow(-1,n-1)*(2*(n-1)+1))
    
def exe(a):
    r = 0
    for i in range(1,int(a)+1):
        r += add(i)
    return 4*r

q = False

while not q:
    a = input("please input the times:")
    if a == 'q':
        q = not q
    elif int(a) % 1 == 0:
        print(exe(a))


