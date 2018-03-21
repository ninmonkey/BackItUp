app_config = {
    "source_dir": r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data",
    "dest_dir": r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_output_data",
    "exclude_dirs": [
       r"C:/Users/cppmo_000/Documents/2018/BackItUp/test_input_data/a/skip_me",
        #"C:/",
    ],
    # "exclude_files_globs": [
    #     {"sys files": "*.sys"},
    # ],

    # todo: wcombine `exclude_files` and `exclude_filepaths`
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

}