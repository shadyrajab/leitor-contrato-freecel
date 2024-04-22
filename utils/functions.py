def remove_rbar(x):
    if type(x) is not str:
        return x
    return x.replace("\r", " ")