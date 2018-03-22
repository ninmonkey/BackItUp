import logging
import math
import os
from os.path import getsize, join
import shutil
import time
import logging

from app.config import app_config
from app.locals import (
    files_are_same,
    humanize_bytes,
    print_drive_usage,
)

WHATIF = False
STATS = {} # defaults defined in _reset_stats()
logging.basicConfig(
    filename=os.path.join("logs", "main.log"),
    filemode='w', level=logging.DEBUG)


def _reset_stats():
    STATS["source_total_bytes"] = 0 # number of bytes read from source
    STATS["copied_total_bytes"] = 0 # number of bytes written to dest
    STATS["skipped_total_bytes"] = 0# bytes 'skipped' when file is already existing
    STATS["source_filecount"] = 0   # numbers of source files parsed
    STATS["copied_filecount"] = 0   # number of files copied (not skipped)
    STATS["backup_start"] = 0   # ticks
    STATS["backup_end"] = 0   # ticks

    # STATS["files_blacklisted"] = 0  # blacklist counter

def print_config():
    # logging.log("JSON config")
    raise NotImplementedError("convert config.py to pretty JSON?")

def print_stats():
    msg = (
        "\nStats"
        "\ntotal size of source = {source_total_bytes}"
        "\ntotal size (actually) copied from source = {copied_total_bytes}"
        "\ntotal size (total skipped duplicates) = {skipped_total_bytes}"
        "\ntotal files in source = {source_filecount}"
        "\ntotal files in copied = {copied_filecount}"
        "\nTime taken (in seconds) {time_secs:.04f}"
    ).format(
        source_total_bytes=humanize_bytes(STATS['source_total_bytes']),
        copied_total_bytes=humanize_bytes(STATS['copied_total_bytes']),
        skipped_total_bytes=humanize_bytes(STATS['skipped_total_bytes']),
        source_filecount = STATS['source_filecount'],
        copied_filecount = STATS['copied_filecount'],
        time_secs = STATS["backup_end"] - STATS["backup_start"],
    )
    logging.info("\n"+msg)
    print(msg)

def walk_entry(source_root=None, dest_root=None): # todo: only arg be config?
    # logic entry point
    if not source_root:
        source_root = app_config['source_dir']
    if not dest_root:
        dest_root = app_config['dest_dir']

    _reset_stats()

    STATS["backup_start"] = time.time()

    for root, dirs, files in os.walk(source_root):
        msg = (
            "\nroot = {root}"
            "\ndirs = {dirs}"
            "\nfiles = {files}"
        ).format(
            root=root,
            dirs=dirs,
            files=files,
        )
        logging.debug(msg)

        STATS["source_filecount"] += 1

        # blacklist 1. hardcoded filenames
        for file in files[:]:
            if file in app_config["exclude_files"]:
                print("\tskipping: ", file)
                files.remove(file)

        # blacklist 2. glob/regex filenames todo

        # good files to copy
        for file in files:
            full_path_source = os.path.join(root, file)
            size = os.path.getsize(full_path_source)
            full_path_dest = os.path.join(
                dest_root,
                os.path.relpath(root, source_root),
                file,
            )

            STATS['source_total_bytes'] += size

            # msg = (
            #     "{name} size = {size}"
            # ).format(name=file, size=humanize_bytes(size))
            # logging.debug(msg)

            full_path_dest_dir = os.path.dirname(full_path_dest)

            msg = (
                "\ncopy files"
                "\n\tSource: {full_path_source}"
                "\n\tDest: {full_path_dest_dir}"
            ).format(
                full_path_source=full_path_source,
                full_path_dest_dir=full_path_dest_dir,
            )
            logging.debug(msg)

            if WHATIF:
                print("WhatIf: copy file \n\tfrom = {} \n\t to = {}".format(full_path_source, full_path_dest))
                continue

            if not files_are_same(full_path_source, full_path_dest):
                os.makedirs(full_path_dest_dir, exist_ok=True)
                shutil.copy2(full_path_source, full_path_dest_dir)
                STATS["copied_total_bytes"] += size
                STATS["copied_filecount"] += 1
            else:
                STATS["skipped_total_bytes"] += size

        for cur_dir in dirs:
            full_dir_path = os.path.join(root, cur_dir)

            # blacklist 3. fullpath dirs
            # print("\n\ttest to exclude: \n\t{}".format(full_dir_path))
            for path in app_config["exclude_dirs"]:
                # print("\tvs:\n\t{}".format(path))

                # if full_dir_path == path: # this failed when mixed slashes for/back
                if os.path.normpath(full_dir_path) == os.path.normpath(path):
                    print("Skipping blacklisted directory = {}".format(path))
                    logging.info("Skipping blacklisted directory = {}".format(path))
                    dirs.remove(cur_dir)
                    continue

            try:
                os.makedirs(full_dir_path)
            except FileExistsError: # wait do I want this? obsolete requirement?
                pass

    STATS["backup_end"] = time.time()

if __name__ == "__main__":
    logging.info("Config name = {}".format(app_config['name']))
    print("WhatIf mode: {}".format(WHATIF))
    print_drive_usage(app_config["source_dir"])
    # print_drive_usage(app_config["dest_dir"])
    print_drive_usage(r"D:\temp_backup_test")

    # walk_entry()
    walk_entry(app_config["source_dir"], app_config["dest_dir"])
    # walk_entry(app_config["source_dir"], r"D:\temp_backup_test")

    print_stats()
    print("\nDone.")

