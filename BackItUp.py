from os.path import getsize, join
import logging
import logging
import math
import os
import shutil
import time

# from app.config import app_config, load_config
import app.config
from app.app_locals import (
    files_are_same,
    humanize_bytes,
    print_drive_usage,
)

import app
from app import config

NTFS_LENGTH_LIMIT = 260
DISABLE_CONSOLE_IO = True # todo: test for speed
WHATIF = False   # if True, disables writing
STATS = {
    "backup_end": 0,
    "backup_start": 0,       # seconds
    "copied_filecount": 0,   # number of files copied (not skipped)
    "copied_total_bytes": 0, # number of bytes written to dest
    "skipped_total_bytes": 0,# bytes 'skipped' when file is already existing
    "source_filecount": 0,   # numbers of source files parsed
    "source_total_bytes": 0, # number of bytes read from source
}
MISSED_FILES = []

# logging.basicConfig(
#     filename=os.path.join("logs", "main.log"),
#     filemode='w', level=logging.DEBUG)

logging.basicConfig(
    handlers=[logging.FileHandler(os.path.join("logs", "main.log"), 'w', 'utf-8')],
    level=logging.DEBUG)


def _reset_stats():
    STATS["backup_end"] = 0         # seconds
    STATS["backup_start"] = 0       # seconds
    STATS["copied_filecount"] = 0   # number of files copied (not skipped)
    STATS["copied_total_bytes"] = 0 # number of bytes written to dest
    STATS["skipped_total_bytes"] = 0# bytes 'skipped' when file is already existing
    STATS["source_filecount"] = 0   # numbers of source files parsed
    STATS["source_total_bytes"] = 0 # number of bytes read from source
    # STATS["files_blacklisted"] = 0  # blacklist counter
    MISSED_FILES = []

def print_config():
    # logging.log("JSON config")
    raise NotImplementedError("convert config.py to pretty JSON?")

def print_stats(stats):
    msg_stats = (
        "\nStats"
        "\ntotal size of source = {source_total_bytes}"
        "\ntotal size (actually) copied from source = {copied_total_bytes}"
        "\ntotal size (total skipped duplicates) = {skipped_total_bytes}"
        "\ntotal files in source = {source_filecount}"
        "\ntotal files in copied = {copied_filecount}"
        "\nTime taken (in seconds) {time_secs:.3f}"
    ).format(
        source_total_bytes=humanize_bytes(stats['source_total_bytes']),
        copied_total_bytes=humanize_bytes(stats['copied_total_bytes']),
        skipped_total_bytes=humanize_bytes(stats['skipped_total_bytes']),
        source_filecount = stats['source_filecount'],
        copied_filecount = stats['copied_filecount'],
        time_secs = stats["backup_end"] - stats["backup_start"],
    )

    msg = "Missing files from (>= 260) limit:"
    for file in MISSED_FILES:
        msg += "\nfile: {}".format(file)
    msg += "\nMissing {} files".format(len(MISSED_FILES))
    logging.warning("\n{}\n".format(msg))
    print(msg)

    logging.info("\n{}\n".format(msg_stats))
    print(msg_stats)

def walk_entry(app_config): # todo: only arg be config?
    # logic entry point
    source_root = app_config['source_dir']
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

        # blacklist
        for file in files[:]:
            # 1. hardcoded filenames
            if file in app_config["exclude_files"]:
                logging.debug("{}".format(os.path.join(root, file)))
                logging.debug("\tskipping: {}".format(file))
                files.remove(file)

            # todo: blacklist 2. /regex filenames

        # good files to copy
        for file in files:
            full_path_source = os.path.normpath(os.path.join(root, file))
            full_path_dest = os.path.normpath(os.path.join(
                dest_root,
                os.path.relpath(root, source_root),
                file,
            ))

            if len(full_path_source) >= NTFS_LENGTH_LIMIT:
                # msg = "Could not backup filepath with length >= 260 for full_path_source:\n\t{0}\n\tlen={1})".format(full_path_source, len(full_path_source))
                # logging.error(msg)
                # print(msg)
                # print("len=", len(full_path_source))
                # MISSED_FILES.append(full_path_source)
                full_path_source = "\\\\?\\" + full_path_source
                full_path_dest = "\\\\?\\" + full_path_dest


            size = os.path.getsize(full_path_source)
            # size = 1

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
            if not DISABLE_CONSOLE_IO:
                print(msg)

            msg = (
                "\nfull path  srd: {full_src}"
                "\nfull path dest: {full_dest}"
                "\nfull path dest_dir: {full_dir}"
                "\n"
            ).format(
                full_src=full_path_source,
                full_dest=full_path_dest,
                full_dir=full_path_dest_dir,
            )
            logging.debug(msg)
            # if not DISABLE_CONSOLE_IO:
                # print(msg)

            if WHATIF:
                # print("WhatIf: copy file \n\tfrom = {} \n\t to = {}".format(full_path_source, full_path_dest))
                continue

            if not files_are_same(full_path_source, full_path_dest):

                # if len(full_path_dest) >= NTFS_LENGTH_LIMIT or len(full_path_dest_dir) >= NTFS_LENGTH_LIMIT:
                #     msg = "Could not backup filepath with length >= 260 for full_path_dest:\n\t{})".format(full_path_dest)
                #     logging.error(msg)
                #     print(msg)
                #     MISSED_FILES.append(full_path_source)
                #     continue

                # if full_path_dest_dir == "D:\\backup_2018 automatic nin.BackItUp\\.gradle\\caches\\2.2.1\\scripts\\asLocalRepo1565470307841526719_bqvpis3d6e1pxv0ur2vf6ycam\\InitScript\\no_initscript\\classes":
                #     print("^"*100)
                #     print("src: ", len(full_path_source))
                #     print("dest file: ", len(full_path_dest))
                #     print("dest dir: ", len(full_path_dest_dir))
                #     continue

                # print("len: ", len(full_path_dest_dir))

                os.makedirs(full_path_dest_dir, exist_ok=True)
                shutil.copy2(full_path_source, full_path_dest_dir)
                # if not DISABLE_CONSOLE_IO:
                print("+", end='', flush=True)# flush=True

                STATS["copied_total_bytes"] += size
                STATS["copied_filecount"] += 1
            else:
                STATS["skipped_total_bytes"] += size

                # if not DISABLE_CONSOLE_IO:
                # print(".", end='', flush=True)# flush=True

        for cur_dir in dirs[:]:
            full_dir_path = os.path.join(root, cur_dir)

            # blacklist 3. fullpath dirs
            # print("\n\ttest to exclude: \n\t{}".format(full_dir_path))
            for path in app_config["exclude_dirs"]:
                # print("\tvs:\n\t{}".format(path))

                # if full_dir_path == path: # this failed when mixed slashes for/back
                if os.path.normpath(full_dir_path) == os.path.normpath(path):
                    # print("Skipping blacklisted directory = {}".format(path))
                    logging.debug("Skipping blacklisted directory = {}".format(path))
                    dirs.remove(cur_dir)
                    continue

            if not os.path.isdir(full_dir_path):
                os.makedirs(full_dir_path)

    STATS["backup_end"] = time.time()

def run(config_name):
    app_config = config.load_config(config_name)
    msg = "Config name = {}".format(app_config['name'])
    print(msg)
    logging.info(msg)

    print("WhatIf mode: {}".format(WHATIF))
    print_drive_usage(app_config["source_dir"])
    print_drive_usage(app_config["dest_dir"])
    walk_entry(app_config)
    print_stats(STATS)
    print("Done: config = {config_name}".format(config_name=config_name))

if __name__ == "__main__":

    run("debug")
    # run("jake_backup 2018")

    print("\nDone.")

