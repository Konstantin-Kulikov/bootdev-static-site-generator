import os
import shutil


def clear_folder(path):
    path_content = os.listdir(path)
    for i in path_content:
        i = os.path.join(path, i)
        if os.path.isfile(i):
            os.remove(i)
        else:
            shutil.rmtree(i)            


def collect_filenames(path):
    result = []
    if os.path.isfile(path):
        result.append(path)
    else:
        for name in os.listdir(path):
            if os.path.isfile(name):
                result.append(name)
            else:
                result.extend(collect_filenames(os.path.join(path, name)))
    return result


def copy_content(src, destination):
    clear_folder(destination)
    src_filenames = collect_filenames(src)
    target_filenames = []
    for filename in src_filenames:
        filename = filename.replace(src, '')
        filename = filename.lstrip('/')
        target_filenames.append(filename)
    for target in target_filenames:
        result = destination
        for part in target.split('/'):
            if '.' in part:
                shutil.copy(os.path.join(src, target), os.path.join(result, part))
            else:
                subdir = os.path.join(result, part)
                if not os.path.exists(subdir):
                    os.mkdir(subdir)
                    result = subdir
                else:
                    result = os.path.join(result, part)

    