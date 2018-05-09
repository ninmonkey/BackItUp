# BackItUp

Easy to use program to backup data.

todo

- extra logging on failure of 
 
    `os.path.walk()` exception try block: set `exc_info=True`
         
- path blacklist using REGEX, eg: "^[.].*"
    - then manual whitelist applies *after*
- count stats how many files (and size) are updated
    (dest exists, yet source edited) 
- example config

# USING_WINDOWS

If `USING_WINDOWS` is True, paths will use NTFS long filenames which may exceed 260 characters.

# test cases for I/O speed:

test cases to write for speed

## 0. no logs
    
disable all `print()` and `logging()`
    
## 1. redundant makedirs

    iteration dirs, always calling 
        os.makedirs(, exist_ok=True)
    
## 2. cache

    getsize()
    
## 3. path manipulation

    os.path.basename()
    os.path.normpath()
    os.path.relpath()