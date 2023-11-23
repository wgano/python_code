class Solution:
    def isValid(self, s: str) -> bool:
        L = ["(","[","{"]
        R = [")","]","}"]
        l = ["0"]
        _l,_r = 0,0
        if len(s)%2 != 0:
            return False
        for step in s:
            if step in L:
                _l += 1
                if step == "(":
                    l.append("1")
                if step == "[":
                    l.append("2")
                if step == "{":
                    l.append("3")
            if step in R:
                _r += 1
                if step == ")":
                    d = l.pop()
                    if d == "1":
                        continue
                    else:return False

                if step == "]":
                    d = l.pop()
                    if d == "2":
                        continue
                    else:return False

                if step == "}":
                    d = l.pop()
                    if d == "3":
                        continue
                    else:return False
        if _l != _r:
            return False
        
        return True
