



def golinit():
    global _global_dict
    _global_dict = {}


def set_value(key,value):
    _global_dict[key] = value


def get_value(key,defValue=None):
    try:
        return _global_dict[key]
    except KeyError:
        return defValue