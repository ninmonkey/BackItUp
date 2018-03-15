import math
import shutil
import os
from os.path import getsize, join

WHATIF = False

app_config = {
    "source_dir":"C:/Users/cppmo_000/Documents/2017/BackItUp/test_input_data",
    "dest_dir":"C:/Users/cppmo_000/Documents/2017/BackItUp/test_output_data",
    "exclude_dirs": [
       "C:/Users/cppmo_000/Documents/2017/BackItUp/test_input_data/a/skip_me",
        #"C:/",
    ],
    # "exclude_files_globs": [
    #     {"sys files": "*.sys"},
    # ],

    # todo: wcombine `exclude_files` and `exclude_filepaths`
        # by allowing REGEX or even just GLOBs
    # global excludes ignoring paths
    "exclude_files": [
       "pagefile.sys",
       "swapfile.sys",
       "hiberfil.sys",
        # recycle bin?,
    ],

    # exclusions by path
    # "exclude_filepaths": [
    #     r"C:/Users/cppmo_000/AppData/Roaming",
    # ]

}

STATS = {
    "source_total": 0,
    "copied_total": 0,
    "skipped_total": 0,
    "source_files": "NYI",
    "copied_files": "NYI",
}

def humanize_bytes(num_bytes, suffix='B'):
    num = num_bytes
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "{num:.1f}{unit}{suffix}".format(num=num, unit=unit, suffix=suffix)
        num /= 1024.0
    return "{num:.1f}{unit}{suffix}".format(num=num, unit='Yi', suffix=suffix)

def print_drive_usage(drive="c:"):
    disk_usage = shutil.disk_usage(drive)
    msg = (
        "\nDrive: {drive}"
        "\nTotal: {total} [{free_percent:0.0f}% free]"
        "\nUsed: {used}"
        "\nFree: {free}"
    ).format(
        drive=os.path.splitdrive(drive)[0],
        total=humanize_bytes(disk_usage.total),
        used=humanize_bytes(disk_usage.used),
        free=humanize_bytes(disk_usage.free),
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

        # todo: raise Exception("Last: 1] filter glob 2] copy file ! WHATIF")

        # blacklist
        for file in files[:]:
            if file in app_config["exclude_files"]:
                files.remove(file)

        for file in files:
            # print("x {}".format(file))


            full_path_source = os.path.join(root, file)
            full_path_dest = os.path.join(root, file)
            size = os.path.getsize(full_path_source)
            STATS['source_total'] += size

            msg = (
                "{name} size = {size}"
            ).format(name=file, size=humanize_bytes(size))
            print(msg)

            msg = (
                "\ncopy files"
                "\n\tSource: {src}"
                "\n\tDest: {dest}"
            ).format(
                src=full_path_source,
                dest=full_path_dest,
            )
            print(msg)

            # filter_filenames = [r"C:\pagefile.sys"]

            if WHATIF:
                pass
            else:
                pass

        for cur_dir in dirs:
            full_dir = os.path.join(root, cur_dir)

            # ignore dirs
            if full_dir in app_config["exclude_dirs"]:
                print("\tskip: ", cur_dir)
                dirs.remove(cur_dir)
                # todo: Or use del cur_dir # or similar
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
        "\ntotal size of source = {total}"
        "\ntotal size (actually) copied from source = {total_copied}"
        "\ntotal size (total skipped duplicates) = {total_skipped}"
    ).format(
        total=humanize_bytes(STATS['source_total']),
        total_copied=humanize_bytes(STATS['copied_total']),
        total_skipped=humanize_bytes(STATS['skipped_total']),
    )
    print(msg)
    print("Done.")

