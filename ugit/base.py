import os
from . import data

def write_tree(directory='.'):
    entries = []
    with os.scandir(directory) as it:
        for entry in it:
            full = f'{directory}/{entry.name}'
            if is_ignored(full):
                continue
            oid = None  # Initialize oid with a default value
            type_ = None  # Initialize type_ with a default value
            if entry.is_file(follow_symlinks=False):
                type_ = 'blob'
                with open(full, 'rb') as f:
                    oid = data.hash_object(f.read())
            elif entry.is_dir(follow_symlinks=False):
                type_ = 'tree'
                oid = write_tree(full)
            if oid is not None:  # Check if oid is bound before appending
                entries.append((entry.name, oid, type_))

    tree = ''.join(f'{type_} {oid} {name}\n' for name, oid, type_ in sorted(entries))
    return data.hash_object(tree.encode(), 'tree')

def is_ignored(path):
    return '.ugit' in path.split('/')
