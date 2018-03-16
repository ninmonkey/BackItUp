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

STATS = {} # defaults in _reset_stats()

def _reset_stats():
    STATS["source_total_bytes"] = 0
    STATS["copied_total_bytes"] = 0
    STATS["skipped_total_bytes"] = 0
    STATS["source_filecount"] = 0
    STATS["copied_filecount"] = 0
    STATS["files_blacklisted"] = 0


def print_stats():
    msg = (
        "\nStats"
        "\ntotal size of source = {source_total_bytes}"
        "\ntotal size (actually) copied from source = {copied_total_bytes}"
        "\ntotal size (total skipped duplicates) = {skipped_total_bytes}"
        # "\ntotal files in source = {source_filecount}"
        # "\ntotal files in source = {source_filecount}"
    ).format(
        source_total_bytes=humanize_bytes(STATS['source_total_bytes']),
        copied_total_bytes=humanize_bytes(STATS['copied_total_bytes']),
        skipped_total_bytes=humanize_bytes(STATS['skipped_total_bytes']),
        # total_skipped=humanize_bytes(STATS['source_filecount']),
    )
    print(msg)

def walk_entry(source_root=None, dest_root=None):
    # logic entry point
    if not source_root:
        source_root = app_config['source_dir']
    if not dest_root:
        dest_root = app_config['dest_dir']

    _reset_stats()

    for root, dirs, files in os.walk(source_root):
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
                print("\tskipping: ", file)
                files.remove(file)
            # todo: 1] filter glob

        for file in files:
            full_path_source = os.path.join(root, file)
            size = os.path.getsize(full_path_source)
            full_path_dest = os.path.join(
                dest_root,
                os.path.relpath(root, source_root),
                file,
            )

            STATS['source_total_bytes'] += size

            msg = (
                "{name} size = {size}"
            ).format(name=file, size=humanize_bytes(size))
            # print(msg)

            msg = (
                "\ncopy files"
                "\n\tSource: {full_path_source}"
                "\n\tDest: {full_path_dest}"
            ).format(
                full_path_source=full_path_source,
                full_path_dest=full_path_dest,
            )
            print(msg)

            if WHATIF:
                print("WhatIf: copy file \n\tfrom = {} \n\t to = {}".format(full_path_source, full_path_dest))
                continue

            print("src = {}".format(full_path_source))
            print("dst = {}".format(full_path_dest))
            if not os.path.exists(full_path_dest):
                print("NOT exists = {}".format(full_path_dest))
            else:
                print("exists = {}".format(full_path_dest))

            full_path_dest_dir = os.path.dirname(full_path_dest)
            os.makedirs(full_path_dest_dir, exist_ok=True)
            shutil.copy2(full_path_source, full_path_dest)

        for cur_dir in dirs:
            full_dir_path = os.path.join(root, cur_dir)

            # ignore dirs
            if full_dir_path in app_config["exclude_dirs"]:
                print("\tskipping: {}".format(cur_dir))
                dirs.remove(cur_dir)
                # todo: Or use del cur_dir # or similar
                continue
            try:
                os.makedirs(full_dir_path)
            except FileExistsError:
                pass

if __name__ == "__main__":
    print("WhatIf mode: {}".format(WHATIF))
    print_drive_usage(app_config["source_dir"])
    print_drive_usage(app_config["dest_dir"])
    print_drive_usage(r"D:\temp_backup_test")

    # walk_entry()
    walk_entry(app_config["source_dir"], app_config["dest_dir"])
    # walk_entry(app_config["source_dir"], r"D:\temp_backup_test")

    print_stats()
    print("Done.")

