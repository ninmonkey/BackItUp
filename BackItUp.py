import math
import shutil

# const
BYTES_TO_MB = 1 / (1024**2)
BYTES_TO_GB = 1 / (1024**3)
BYTES_TO_TB = 1 / (1024**4)

app_config = [
    {
        "root_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data",
        "dest_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_output_data",
        "exclude_dirs": [r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data\a\skip_me"],
    },
]

def human_readable_size(num_bytes):
    # human-readable units for bytes
    if num_bytes == 0:
        return "0B"
    size_name = size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(num_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(num_bytes / p, 2)
    return "{size:.2f} {unit}".format(size=s, unit=size_name[i])

def print_usage(drive="c:"):
    disk_usage = shutil.disk_usage(drive)
    msg = (
        "\n{drive}"
        "\nTotal: {total}"
        "\nUsed: {used}"
        "\nFree: {free}"
    ).format(
        drive = drive,
        total = human_readable_size(disk_usage.total),
        used = human_readable_size(disk_usage.used),
        free = human_readable_size(disk_usage.free),
    )
    print(msg)

if __name__ == "__main__":
    print_usage("c:")
    print_usage("d:")


    print("Done.")
