import cx_Freeze

# build command: python export_to_exe.py build
# generate Windows installer: python export_to_exe.py bdist_msi

packages = ["pygame"]
include_files = [("fonts", "fonts"), ("images", "images"), ("LICENSE", "BirdJumper_license.txt"),
                 ("assets.txt", "assets_sources.txt")]

# base="Win32GUI" so the console window does not pop up
executables = [cx_Freeze.Executable("main.py", base="Win32GUI", icon="images/duck-ga9276d9c3_640.ico",
                                    target_name="BirdJumper.exe")]

cx_Freeze.setup(
    name="Bird Jumper",
    version="1.0",
    description="A Flappy Bird rip-off",
    options={
        "build_exe": {
            "packages": packages,
            "include_files": include_files
        }
    },
    executables=executables
)
