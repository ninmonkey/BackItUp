import os
import shutil
import logging

def valid_path(path):
    if not path:
        raise ValueError("Path given is empty")
    if os.path.isdir(path):
        return True

    os.makedirs(path, exist_ok=True)
    return os.path.isdir(path)

def files_are_same(full_path_source, full_path_dest):
    """
    save I/O on duplicate files

    full_path_source:   source path including filename
    full_path_dest:     dest path including filename
    """
    if not os.path.exists(full_path_dest):
        return False

    size_source = os.path.getsize(full_path_source)
    size_dest = os.path.getsize(full_path_dest)
    filename_source = os.path.basename(full_path_source)
    filename_dest = os.path.basename(full_path_dest)

    if size_source != size_dest:
        # logging.debug("size_source != size_dest")
        return False

    if filename_source != filename_dest:
        # logging.debug("filename_source != filename_dest")
        return False

    logging.debug("files_are_same(): {},\nfor source: {}\nfor dest: {}".format(
        True,
        full_path_source,
        full_path_dest)
    )

    return True

def humanize_bytes(num_bytes, suffix='B'):
    # convert byte count to human readable units
    num = num_bytes
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "{num:.1f}{unit}{suffix}".format(num=num, unit=unit, suffix=suffix)
        num /= 1024.0
    return "{num:.1f}{unit}{suffix}".format(num=num, unit='Yi', suffix=suffix)

def print_drive_usage(drive="c:/"):
    # usage stats
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
        free_percent=(disk_usage.free / disk_usage.total) * 100,
    )
    logging.info("\n"+msg+"\n")
    print(msg)