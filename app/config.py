import os.path
from app.app_locals import valid_path

app_config = None
app_config_all = [
    {
        "name": "debug",
        "source_dir": "C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data",
        "dest_dir": "C:/Users/cppmo_000/Documents/2018/BackItUp/test_output_data",

        "exclude_dirs": [
           "C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data/a/skip_me",
        ],
        # "exclude_files_globs": [
        #     "*.pyc",        # todo
        #     "pagefile.sys",
        #     "swapfile.sys",
        #     "hiberfil.sys",
        # ],

        # global excludes ignoring paths
        "exclude_files": [
            "$Recycle.Bin",
            "pagefile.sys",
            "swapfile.sys",
            "hiberfil.sys",
        ],
    },

    {
        "name": "jake_backup",
        "source_dir": "",
        "dest_dir": "",
        "exclude_dirs": [
            "C:/$Recycle.Bin",
            "C:/Users/cppmo_000/Dropbox",
            "C:/Users/cppmo_000/AppData/Roaming/Apple Computer/MobileSync",
            "C:/Users/cppmo_000/Music/iTunes",
            "C:/Users/cppmo_000/Documents/AndroidStudioProjects",
            "C:/Users/cppmo_000/Documents/Battlefield 4",
            "C:/Users/cppmo_000/Documents/creeperworld3",
            "C:/Users/cppmo_000/Documents/Dolphin Emulator",
            "C:/Users/cppmo_000/Documents/Dungeon of the Endless",
            "C:/Users/cppmo_000/Documents/Electronic Arts",
            "C:/Users/cppmo_000/Documents/Games for Windows - LIVE Demos",
            "C:/Users/cppmo_000/Documents/Heroes of the Storm",
            "C:/Users/cppmo_000/Documents/League of Legends",
            "C:/Users/cppmo_000/Documents/my games/Tabletop Simulator",
            "C:/Users/cppmo_000/Documents/PoE-TradeMacro",
            "C:/Users/cppmo_000/Documents/SEGA",
            "C:/Users/cppmo_000/Documents/UnrealTournament",
            "C:/Users/cppmo_000/Documents/WB Games",
            "C:/Users/cppmo_000/Documents/my games",
        ],
        # # exclude globs / regex
        # "exclude_files_globs": [
        #     # {"sys files": "*.sys"},
        # ],


        # global excludes ignoring paths
        "exclude_files": [
            "$Recycle.Bin",
            "pagefile.sys",
            "swapfile.sys",
            "hiberfil.sys",
        ],
    },

]

def validate_config(config):
    # basic validate config file, check directories
    if not config:
        raise ValueError("No config given!")

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
            validate_config(config)
            return config
    raise ValueError("Unknowing config name = {}".format(name))


