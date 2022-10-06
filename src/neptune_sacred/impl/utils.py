from flatten_dict.flatten_dict import flatten


def flatten_space_reducer(k1, k2):
    if k1 is None:
        return k2
    else:
        return f"{k1} {k2}"


def custom_flatten_dict(d):
    return flatten(d, reducer=flatten_space_reducer)
