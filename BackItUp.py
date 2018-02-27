import math
import shutil
import os
from os.path import join

# const
# BYTES_TO_MB = 1 / (1024**2)
# BYTES_TO_GB = 1 / (1024**3)
# BYTES_TO_TB = 1 / (1024**4)

app_config = {
    "source_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data",
    "dest_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_output_data",
}
    # "exclude_dirs": [r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data\a\skip_me"],



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


if __name__ == "__main__":
    print_drive_usage("c:")
    # print_drive_usage("d:")

    print("usage:")
    print_drive_usage(r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data")
    # print_usage(app_config["source_dir"])
    test_listdir()


    print("Done.")
