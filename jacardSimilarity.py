# expects to term frequency vectors or term conatining vecotr
def jacardSimilairty(a, b):
    intersection = 0
    union = 0
    for i in range(len(a)):
        intersection = (a[i] > 0 and b[i] > 0)
        union = (a[i] > 0 or b[i] > 0)
    return intersection/union