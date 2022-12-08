a = input("请输入行数:")
b = []
v = []
for i in range(0, int(a)):
    b.append(0)
    v.append(0)
b[0] = 1
v[0] = 1
for j in range(1, int(a)+1):
    if j % 2 == 0:
        for x in range(1, int(j)+1):
            if x == 1:
                m = 1
            else:
                m = b[x-2] + b[x-1]
            print(m, " ", end="")
            v[x-1] = m
    else:
        for y in range(1, int(j)+1):
            if y == 1:
                m = 1
            else:
                m = v[y-2] + v[y-1]
            print(m, " ", end="")
            b[y-1] = m
    print("\n")

