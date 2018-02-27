import math
import shutil
# from os.path import join
# import os.path.getsize
import os
from os.path import getsize, join

# const
# BYTES_TO_MB = 1 / (1024**2)
# BYTES_TO_GB = 1 / (1024**3)
# BYTES_TO_TB = 1 / (1024**4)

app_config = {
    "source_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data",
    "dest_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_output_data",
    "exclude_dirs": [
        r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data\a\skip_me",
        r"C:\\",
    ],
}

STATS = {
    "source_total": 0,
    "copied_total": "NYI",
    "skipped_total": "NYI",
}


# def human_readable_size2(num_bytes):
#     # human-readable units for bytes
#     if num_bytes == 0:
#         return "0B"
#     size_name = size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
#     i = int(math.floor(math.log(num_bytes, 1024)))
#     p = math.pow(1024, i)
#     s = round(num_bytes / p, 2)
#     return "{size:.2f} {unit}".format(size=s, unit=size_name[i])

def human_readable_size(num_bytes, suffix='B'):
    num = num_bytes
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "{num:.2f}{unit}{suffix}".format(num=num, unit=unit, suffix=suffix)
        num /= 1024.0
    return "{num:.2f}{unit}{suffix}".format(num=num, unit='Yi', suffix=suffix)

def print_drive_usage(path="c:"):
    disk_usage = shutil.disk_usage(path)
    msg = (
        "\n{path}"
        "\nTotal: {total} [{free_percent:0.0f}% free]"
        "\nUsed: {used}"
        "\nFree: {free}"
    ).format(
        path=path,
        total=human_readable_size(disk_usage.total),
        used=human_readable_size(disk_usage.used),
        free=human_readable_size(disk_usage.free),
        free_percent=(disk_usage.free / disk_usage.total) * 100
    )
    print(msg)

def test_listdir(src=None, dest=None):
    # sort of from: https://docs.python.org/3.1/library/shutil.html?highlight=shutil#example
    if not src:
        src = app_config['source_dir']
    if not dest:
        dest = app_config['dest_dir']
    names = os.listdir(src)

    msg = (
        "\nsrc = {src}"
        "\ndest = {dest}"
        "\ndirs = {dirs}"
    ).format(src=src, dest=dest, dirs=names)
    print(msg)
    try:
        os.makedirs(dest)
    except FileExistsError:
        pass

    # source_path = os.path.join(src, names)

def test_walk(src=None, dest=None):
    if not src:
        src = app_config['source_dir']
    if not dest:
        dest = app_config['dest_dir']

    for root, dirs, files in os.walk(src):
        # all files in dir:
        # print(sum(getsize(join(root, name)) for name in files), end=" ")
        msg = (
            "\nroot = {root}"
            "\ndirs = {dirs}"
            "\nfiles = {files}"
        ).format(
            root=root,
            dirs=dirs,
            files=files
        )
        print(msg)

        for file in files:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            msg = (
                "{name} = {size}"
            ).format(name=file, size=size)
            print(msg)
            STATS['source_total'] += size

        # ignore dirs
        for dir in dirs:
            full_dir = os.path.join(root, dir)
            if full_dir in app_config["exclude_dirs"]:
                print("skip ", dir)
                dirs.remove(dir)

if __name__ == "__main__":
    print_drive_usage("c:")
    # print_drive_usage("d:")

    print("usage:")
    print_drive_usage(r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data")
    # print_usage(app_config["source_dir"])
    test_walk()


    msg = (
        "\nStats"
        "\ntotal usage of source= {total}"
        "\ntotal (actually) copied of source= {total_copied}"
        "\ntotal (total skipped duplicates) = {total_skipped}"
    ).format(
        total=human_readable_size(STATS['source_total']),
        total_copied='NYI', # human_readable_size(STATS['copied_total']),
        total_skipped='NYI' # human_readable_size(STATS['skipped_total']),
    )
    print(msg)
    print("Done.")

