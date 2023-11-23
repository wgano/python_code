from pythonds.basic.stack import Stack
def infixtopostfix(s):
    dic={"*":3,"/":3,"+":2,"-":2,"(":1}
    sta = Stack()
    res = []
    s = list(s)
    for token in s:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
            res.append(token)
        elif token=='(':
            sta.push(token)
        elif token==')':
            tt = sta.pop()
            while tt!='(':
                res.append(tt)
                tt=sta.pop()
        else:
            while (not sta.isEmpty()) and \
                (dic[sta.peek()]>=dic[token]):
                    res.append(sta.pop())
            sta.push(token)
    while not sta.isEmpty():
        res.append(sta.pop())
    return "".join(res)



def calcualtepostfix(s):
    s = list(infixtopostfix(s))
    k=["+","-","*","/"]
    te = Stack()
    s = list(s)
    for i in s:
        if i not in k:
            te.push(i)
        elif i == "+":
            r = te.pop()
            l = te.pop()
            te.push(str(int(l)+int(r)))
        elif i == "*":
            r = te.pop()
            l = te.pop()
            te.push(str(int(l)*int(r)))
        elif i == "-":
            r = te.pop()
            l = te.pop()
            te.push(str(int(l)-int(r)))
        elif i == "/":
            r = te.pop()
            l = te.pop()
            te.push(str(int(l)/int(r)))
                    
    return te.pop()



print(calcualtepostfix("((((5+7)-4)*6)+5)"))
