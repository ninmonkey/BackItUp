import os.path

app_config = None
app_config_all = [
    {
        "name": "debug",
        "source_dir": r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data",
        "dest_dir": r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_output_data",
        "exclude_dirs": [
           r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data/a/skip_me",
            #"C:/",
        ],
        # "exclude_files_globs": [
        #     {"sys files": "*.sys"},
        # ],

        # by allowing REGEX or even just GLOBs
        # global excludes ignoring paths
        "exclude_files": [
           "pagefile.sys",
           "swapfile.sys",
           "hiberfil.sys",
            # recycle bin?,
        ],

        # exclusions by path
        # "exclude_filepaths": [
        #     r"C:/Users/cppmo_000/AppData/Roaming",
        # ]

    },

    {
        "name": "jake_backup",
        "source_dir": r"",
        "dest_dir": r"",
        "exclude_dirs": [
            r"C:/Users/cppmo_000/Dropbox",
            r"C:/Users/cppmo_000/AppData/Roaming/Apple Computer/MobileSync",
            r"C:/Users/cppmo_000/Music/iTunes",
            r"C:/Users/cppmo_000/Documents/AndroidStudioProjects",
            r"C:/Users/cppmo_000/Documents/Battlefield 4",
            r"C:/Users/cppmo_000/Documents/creeperworld3",
            r"C:/Users/cppmo_000/Documents/Dolphin Emulator",
            r"C:/Users/cppmo_000/Documents/Dungeon of the Endless",
            r"C:/Users/cppmo_000/Documents/Electronic Arts",
            r"C:/Users/cppmo_000/Documents/Games for Windows - LIVE Demos",
            r"C:/Users/cppmo_000/Documents/Heroes of the Storm",
            r"C:/Users/cppmo_000/Documents/League of Legends",
            r"C:/Users/cppmo_000/Documents/my games/Tabletop Simulator",
            r"C:/Users/cppmo_000/Documents/PoE-TradeMacro",
            r"C:/Users/cppmo_000/Documents/SEGA",
            r"C:/Users/cppmo_000/Documents/UnrealTournament",
            r"C:/Users/cppmo_000/Documents/WB Games",
        ],
        # exclude globs / regex
        "exclude_files_globs": [
            {"sys files": "*.sys"},
        ],
        # global excludes ignoring paths
        "exclude_files": [
           "pagefile.sys",
           "swapfile.sys",
           "hiberfil.sys",
            # todo: recycle bin?,
        ],
    }

]

def valid_path(path):
    if not path:
        return False
    return os.path.isdir(path)

def validate_config(config):
    # validate config file
    path_source = config["source_dir"]
    path_dest = config["dest_dir"]
    if not valid_path(path_source) or not valid_path(path_dest):
        raise ValueError("Bad Paths for \nsource = {}\ndest = {}".format(
            path_source, path_dest)
        )
    return True

def load_config(name):
    for config in app_config_all:
        if config["name"] == name:
            return config
    raise ValueError("Unknowing config name = {}".format(name))

app_config = load_config("jake_backup")
app_config = load_config("debug")
validate_config(app_config)

