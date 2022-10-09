import os
from uuid import uuid4


def path_and_rename(instance, filename, path):
    _, extension = os.path.splitext(filename)
    filename = f'{uuid4().hex}{extension}'
    return os.path.join(path, filename)
