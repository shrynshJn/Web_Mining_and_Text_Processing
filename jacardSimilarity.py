def jacardSimilairty(a, b):
    a = set(a)
    b = set(b)
    union = a.union(b)
    intersection = a.intersection(b)
    return (intersection/union)