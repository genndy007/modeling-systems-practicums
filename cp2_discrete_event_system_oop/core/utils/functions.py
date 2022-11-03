from itertools import count


def set_class_instance_id(cls):
    id_number = count(1)
    cls.instance_id = lambda arg: next(id_number)
    return cls
