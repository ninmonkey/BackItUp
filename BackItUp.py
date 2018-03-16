import math
import shutil
import os
from os.path import getsize, join

from app.config import app_config
from app.locals import (
    humanize_bytes,
    print_drive_usage,
)

WHATIF = False

STATS = {
    "source_total": 0,
    "copied_total": 0,
    "skipped_total": 0,
    "source_files": "NYI",
    "copied_files": "NYI",
}

def walk_entry(src=None, dest_root=None):
    # logic entry point
    if not src:
        src = app_config['source_dir']
    if not dest_root:
        dest_root = app_config['dest_dir']

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
            files=files,
        )
        print(msg)


        # blacklist
        for file in files[:]:
            if file in app_config["exclude_files"]:
                files.remove(file)

        for file in files:
            full_path_source = os.path.join(root, file)
            full_path_dest = os.path.join(dest_root, file)
            size = os.path.getsize(full_path_source)
            STATS['source_total'] += size

            msg = (
                "{name} size = {size}"
            ).format(name=file, size=humanize_bytes(size))
            print(msg)

            full_path_dest2 = os.path.join(
                dest_root,
                os.path.relpath(root, src),
                file,
            )

            msg = (
                "\ncopy files"
                "\n\tSource: {src}"
                "\n\tDest: {dest}"
                "\n\tDest2: {dest2}"
            ).format(
                src=full_path_source,
                dest=full_path_dest,
                dest2=full_path_dest2,
            )
            print(msg)


            # import pdb; pdb.set_trace()
            # todo: raise Exception("Last: 1] filter glob 2] copy file ! WHATIF")
            if WHATIF:
                print("WhatIf: copy file \n\tfrom = {} \n\t to = {}".format(full_path_source, full_path_dest))
            else:
                print("copy file \n\tfrom = {} \n\t to = {}".format(full_path_source, full_path_dest2))
                # shutil.copy2(
                #     src=
                #     dst=)
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
    print("WhatIf mode: {}".format(WHATIF))
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

