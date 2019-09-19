import math
def g(x, b):
    r = x%b
    q = int(x/b)

    res = ""
    for k in range(q):
        res = res + "0"
    res = res + "1"

    i = int(math.log(b,2))
    d = int(math.pow(2,i+1) - b)

    if(r>=d):
        r = r + d
        r_b = bin(r).replace("0b","")
        res+=r_b
    else:
        r_b = bin(r).replace("0b","")
        res+=r_b
    print(res)


    for q in range(len(res)):
        if(res[q]=="1"):
            break

    i = int(math.log(b,2))
    d = int(math.pow(2,i+1) - b)

    r = res[q+1:q+i+1]
    print(r)
    r = int(r,2)
    if(r>=d):
        r = res[q+1:q+i+2]
        r = int(r,2)
        r = r - d
    x = q*b + r
    print(x)  
g(14, 10)  