import math
import shutil

BYTES_TO_MB = 1 / (1024**2)
BYTES_TO_GB = 1 / (1024**3)
BYTES_TO_TB = 1 / (1024**4)

app_config = [
    {
        "root_dir": r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data",
        "exclude_dirs": [r"C:\Users\cppmo_000\Documents\2017\BackItUp\test_input_data\a\skip_me"],
    },
]

def human_readable_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "{size:.2f} {unit}".format(size=s, unit=size_name[i])

def print_usage(drive="c:"):
    disk_usage = shutil.disk_usage(drive)
    print("Total on G: {}".format(human_readable_size(disk_usage.total)))
    print("Used on G: {}".format(human_readable_size(disk_usage.used)))
    print("Free on G: {}\n".format(human_readable_size(disk_usage.free)))


# free = shutil.disk_usage("d:")
# print("Free Space on G: = {:.2f} TB".format(free.free * BYTES_TO_TB))

# print("Total on G: {}".format(human_readable_size(free.total)))
# print("Used on G: {}".format(human_readable_size(free.used)))
# print("Free on G: {}".format(human_readable_size(free.free)))

print_usage("c:")
print_usage("d:")


print("Done.")
