def clamp(v, min, max):
    if v < min: 
        return min
    elif v > max: 
        return max
    return v

def lerp(n0, n1, a):
    return ((1.0 - a) * n0) + (a * n1)