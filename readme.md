# BackItUp

Easy to use program to backup data.

# todo

- verify path is non-relative to prevent mistakes
- verify dest_dir has enough space on that drive
- whatif:
    - no transfer
    - calc files new, modified, or skip
    - calc Gb/Mb new, modified, or skip

- count:
    - files updated (overwritten)
    - files new (doesn't exist yet)
    - files skipped (same)
    - Gb/Mb total data to update
    - Gb/Mbytes actually updated
    - time taken
    - average write speed
    - list failed writes: dirs, files, reads, etc
- verify directories existence *before* starting copy [option]
- flag to auto-update file if newer than dest [default: warn]
- verify recursion
- verify exclude directories
- exclude globs
- auto-create dest dirs that don't exist
- test if multiprocessing or threading will decrease time
- make user confirm filepaths

    Are you sure?
    src = src
    dest = dest
    files copied = bytes

# white/blacklisting

## blacklisting:

dirs (full):
    currently require full path match

dirs (relative):
    NYI using wildcards

files (full):
    NYI
files (relative):
    NYI

## whitelisting:

dirs:
    NYI
files:
    NYI