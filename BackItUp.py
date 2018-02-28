import math
import shutil
import os
from os.path import getsize, join

app_config = {
    "source_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data",
    "dest_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_output_data",
    "exclude_dirs": [
        r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data\a\skip_me",
        r"C:\\",
    ],
    "exclude_files_globs": [],
    "exclude_files": [
        r"C:\pagefile.sys",
        r"C:\swapfile.sys",
        r"C:\hiberfil.sys",
        # recycle bin?,
    ],

}

STATS = {
    "source_total": 0,
    "copied_total": "NYI",
    "skipped_total": "NYI",
    "source_files": "NYI",
    "copied_files": "NYI",
}

def human_readable_size(num_bytes, suffix='B'):
    num = num_bytes
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "{num:.2f}{unit}{suffix}".format(num=num, unit=unit, suffix=suffix)
        num /= 1024.0
    return "{num:.2f}{unit}{suffix}".format(num=num, unit='Yi', suffix=suffix)

def print_drive_usage(drive="c:"):
    disk_usage = shutil.disk_usage(drive)
    msg = (
        "\nDrive: {drive}"
        "\nTotal: {total} [{free_percent:0.0f}% free]"
        "\nUsed: {used}"
        "\nFree: {free}"
    ).format(
        drive=os.path.splitdrive(drive)[0],
        total=human_readable_size(disk_usage.total),
        used=human_readable_size(disk_usage.used),
        free=human_readable_size(disk_usage.free),
        free_percent=(disk_usage.free / disk_usage.total) * 100
    )
    print(msg)

def walk_entry(src=None, dest=None):
    # logic entry point
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

        for dir in dirs:
            full_dir = os.path.join(root, dir)
            # ignore dirs
            if full_dir in app_config["exclude_dirs"]:
                print("skip ", dir)
                dirs.remove(dir)
                continue
            try:
                os.makedirs(full_dir)
            except FileExistsError:
                pass

if __name__ == "__main__":
    print_drive_usage(app_config["source_dir"])
    print_drive_usage(app_config["dest_dir"])

    walk_entry()

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

