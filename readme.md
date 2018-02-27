# BackItUp

Easy to use program to backup data.

# todo

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