import os
import shutil
import logging

def humanize_bytes(num_bytes, suffix='B'):
    # convert bytes to human readable unit
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