import functools


def deep_getattr(obj, attr):
    return functools.reduce(getattr, attr.split("."), obj)
