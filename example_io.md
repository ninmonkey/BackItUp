# different file I/O examples.md

# docs:

- https://docs.python.org/3/library/os.path.html
- https://docs.python.org/3/library/pathlib.html#pure-paths
- https://docs.python.org/3.1/library/io.html#i-o-base-classes
- https://docs.python.org/3.1/library/os.html#file-descriptor-operations
- https://docs.python.org/3.1/library/os.html#os.stat

# os
shutil.copy2() : preserves metadata
shutil.copytree() : use copy2
shutil.disk_usage : checks usage of entire drive/mount, not the argument path

# see also REGEX filters

https://stackoverflow.com/a/5141829/341744

# os.stat(path)

 - last mod/creation: https://docs.python.org/3.1/library/os.html#os.stat

# filesize
    >>> info.st_size
    9

    >>> os.path.getsize(path)
    9

shows correct info. File manager in windows appears to always be >= 1k if not 0

# os.path

    >>> os.path.split("c:\\music\\ap\\mahadeva.mp3")
    ('c:\\music\\ap', 'mahadeva.mp3')

    >>> (filepath, filename) = os.path.split("c:\\music\\ap\\mahadeva.mp3")
    >>> filepath
    'c:\\music\\ap'
    >>> filename
    'mahadeva.mp3'

    >>> (shortname, extension) = os.path.splitext(filename)
    >>> shortname
    'mahadeva'
    >>> extension
    '.mp3'

## dir usage:

    >>> os.listdir("c:\\")
    ['AUTOEXEC.BAT', 'boot.ini', 'CONFIG.SYS', 'cygwin',
    ...
    'System Volume Information', 'TEMP', 'WINNT']

    >>> [f for f in os.listdir(dirname)
    ...     if os.path.isfile(os.path.join(dirname, f))]
    ['AUTOEXEC.BAT', 'boot.ini', 'CONFIG.SYS', 'IO.SYS', 'MSDOS.SYS',
    'NTDETECT.COM', 'ntldr', 'pagefile.sys']

    >>> [f for f in os.listdir(dirname)
    ...     if os.path.isdir(os.path.join(dirname, f))]
    ['cygwin', 'docbook', 'Documents and Settings', 'Incoming']

# GLOB / py2

    >>> os.listdir("c:\\music\\_singles\\")
    ['a_time_long_forgotten_con.mp3', 'hellraiser.mp3',
    'kairo.mp3', 'long_way_home1.mp3', 'sidewinder.mp3',
    'spinning.mp3']

    >>> glob.glob('c:\\music\\_singles\\*.mp3')
    ['c:\\music\\_singles\\a_time_long_forgotten_con.mp3',
    'c:\\music\\_singles\\hellraiser.mp3',
    'c:\\music\\_singles\\kairo.mp3',
    'c:\\music\\_singles\\long_way_home1.mp3',
    'c:\\music\\_singles\\sidewinder.mp3',
    'c:\\music\\_singles\\spinning.mp3']

    >>> glob.glob('c:\\music\\_singles\\s*.mp3')
    ['c:\\music\\_singles\\sidewinder.mp3',
    'c:\\music\\_singles\\spinning.mp3']

    >>> glob.glob('c:\\music\\*\\*.mp3')

# os.walk(top, topDown=True, ...)

    > When topdown is True, the caller can modify the dirnames list in-place (perhaps using del or slice assignment), and walk() will only recurse into the subdirectories whose names remain in dirnames; this can be used to prune the search, impose a specific order of visiting, or even to inform walk() about directories the caller creates or renames before it resumes walk() again. Modifying dirnames when topdown is False is ineffective, because in bottom-up mode the directories in dirnames are generated before dirpath itself is generated.

https://docs.python.org/3/library/os.html#os.walk

When topdown is True, the caller can modify the dirnames list in-place (perhaps using del or slice assignment), and walk()

# refs

- http://www.diveintopython3.net/files.html
- http://www.diveintopython.net/file_handling/os_module.html