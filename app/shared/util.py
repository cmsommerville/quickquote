import functools


def list_to_dict(l, key):
    return {item['key'] for item in l}


def deep_getattr(obj: dict, attr: str):
    return functools.reduce(getattr, attr.split("."), obj)
