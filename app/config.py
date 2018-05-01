import os.path

from .app_locals import valid_path

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
            "NTUSER.DAT",
            "ntuser.dat.LOG1",
            "ntuser.dat.LOG2",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TM.blf",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TMContainer00000000000000000001.regtrans-ms",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TMContainer00000000000000000002.regtrans-ms",
            "ntuser.ini",
            "ntuser.pol",
        ],
    },

    {
        "name": "jake_backup 2018",
        "source_dir": "C:/Users/cppmo_000",
        # "source_dir": "C:/Users/cppmo_000/.gradle",
        # "source_dir": "C:/Users/cppmo_000/Documents/0x7df/GitHub",
        "dest_dir": "D:/backup_2018 automatic nin.BackItUp",
        "exclude_dirs": [
            "C:/$Recycle.Bin",
            # "C:/Users/cppmo_000/.gradle",
            "C:/Users/cppmo_000/3D Objects",
            "C:/Users/cppmo_000/",
            "C:/Users/cppmo_000/AppData",
            "C:/Users/cppmo_000/AppData/Local/Microsoft",
            "C:/Users/cppmo_000/AppData/Roaming/Apple Computer",
            "C:/Users/cppmo_000/AppData/Roaming/Apple Computer/MobileSync",
            "C:/Users/cppmo_000/Desktop",
            "C:/Users/cppmo_000/Documents/AndroidStudioProjects",
            "C:/Users/cppmo_000/Documents/creeperworld3",
            "C:/Users/cppmo_000/Documents/Dolphin Emulator",
            "C:/Users/cppmo_000/Documents/Dungeon of the Endless",
            "C:/Users/cppmo_000/Documents/Games for Windows - LIVE Demos",
            "C:/Users/cppmo_000/Documents/Heroes of the Storm",
            "C:/Users/cppmo_000/Documents/League of Legends",
            "C:/Users/cppmo_000/Documents/my games",
            "C:/Users/cppmo_000/Documents/my games/Tabletop Simulator",
            "C:/Users/cppmo_000/Documents/PoE-TradeMacro",
            "C:/Users/cppmo_000/Documents/SEGA",
            "C:/Users/cppmo_000/Documents/UnrealTournament",
            "C:/Users/cppmo_000/Documents/WB Games",
            "C:/Users/cppmo_000/Dropbox",
            "C:/Users/cppmo_000/Music/iTunes",
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
            "NTUSER.DAT",
            "ntuser.dat.LOG1",
            "ntuser.dat.LOG2",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TM.blf",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TMContainer00000000000000000001.regtrans-ms",
            "NTUSER.DAT{8a3f97ca-0156-11e8-89e1-00249b0e8d67}.TMContainer00000000000000000002.regtrans-ms",
            "ntuser.ini",
            "ntuser.pol",
        ],
    },

]


def validate_config(config, strict=True):
    # basic validate config file, check directories
    if not config:
        raise ValueError("No config given!")

    path_source = config["source_dir"]
    path_dest = config["dest_dir"]
    if not valid_path(path_source) or not valid_path(path_dest):
        raise ValueError("Bad Paths for \nsource = {}\ndest = {}".format(
            path_source, path_dest)
        )

    if strict:
        for dir in config["exclude_dirs"]:
            if not os.path.isdir(dir):
                print("{}".format(dir))
                raise ValueError("Might be a typo. Path doesn't exist: {}".format(dir))

    return True


def load_config(name):
    for config in app_config_all:
        if config["name"] == name:
            validate_config(config)
            return config

    raise ValueError("Unknowing config name = {}".format(name))


