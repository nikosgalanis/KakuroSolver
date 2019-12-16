import sys

#return the neighbors of n, given the list of variables in the same line/column
def group_consecutives(n, vals, step=1):
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + step
    for i in result:
        if n in i:
            return i

#return the intersection of 2 lists
def intersect(a, b):
    return list(set(a).intersection(b))

#return the union of 2 lists
def Union(a, b):
    return list(set(a) | set(b))
