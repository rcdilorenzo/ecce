import os

def relative_path(current_file, path):
    return os.path.join(os.path.dirname(current_file), path)
