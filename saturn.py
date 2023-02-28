


import os, json, time, sys, platform, zipfile, shutil
from utils.version import getVersion
from utils.Ages import Ages
from utils.Databin import Databin
#from utils.Prefab_Characters import Prefab_Characters
from utils.plugins.common import *

osn = platform.system()
if osn == "nt" or "Linux":
    pass
else:
    print(f"\n\n[!] Error: Unsupported OS: {osn}\n\n")
    time.sleep(3)
    pause()
    sys.exit()

config_path = os.path.join("config", "config.json")
setTitle(f"Saturn {getVersion()}")

"""

Saturn Skin Generator v1.0 (Supports Arena of Valor Game Patch 1.49.1 etc.)
Author  : Curelight (wrxyut)
Github  : https://github.com/wrxyut
Discord : Wrxyut#0880
Url     : 

Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).
You are free to modify this source.

"""

assets_dir = 'assets'
output_dir = 'output'
parent_dir = f'com.garena.game.kgth/files/Resources/{getVersion()}'
ages = 'Ages/Prefab_Characters/Prefab_Hero'
databin = 'Databin/Client'
prefab_characters = 'Prefab_Characters'
directories = [parent_dir, os.path.join(parent_dir, ages), 
               os.path.join(parent_dir, databin), 
               os.path.join(parent_dir, prefab_characters)]

printCredit("wrxyut")
time.sleep(2.5)
clear()
def main():
    # Start 
    # Check if the output directory exists, if not create it and any subdirectories
    created_dirs = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        for directory in directories:
            directory_path = os.path.join(output_dir, directory)
            os.makedirs(directory_path)
            created_dirs.append(directory_path)

        # Print only the directories that were created
        if created_dirs:
            SlowPrint("Created the following directories:")
            print()
            for directory in created_dirs:
                print(directory.replace("\\", "/"))
        time.sleep(2.5)
        clear()


    # Prompt user for input values
    banner()
    SkinId = str(input("    SKIN ID : "))
    ReturnCityEffect = str(input("    Recall Effect : "))
    SoundEffect = str(input("    Sound Effect : "))


    # Load hero data from a configuration file
    clear()
    banner()
    try:

        with open(config_path, "r") as config:
            config = json.load(config)

        # Extract hero ID and naming convention from hero skin ID
        heroId = SkinId[:-2]
        NAME_CASE1 = config[heroId]['NAME_CASE1']
        NAME_CASE2 = config[heroId]['NAME_CASE2']
    
    except Exception as e:
        print(f"\n\n[!] ERROR: Could not read configuration file: {e}\n\n")
        pause()
        sys.exit()
        

    try:

        #
        if heroId in config.keys():
            try:
                clear()
                banner()

                wrxyut = Ages(getVersion(), assets_dir, output_dir, parent_dir, ages, heroId, SkinId, NAME_CASE1, NAME_CASE2, ReturnCityEffect)
                wrxyut.do_ages()

                if SoundEffect.lower() == "y":
                    wrxyut = Databin(assets_dir, output_dir, parent_dir, databin, heroId, SkinId)
                    wrxyut.do_sound(wrxyut.sound_format(f"{heroId}00"), wrxyut.sound_format(SkinId))
                    setTitle(f"Saturn {getVersion()}")

                with zipfile.ZipFile(f'output/{SkinId}-curelight.zip', 'w', compression=zipfile.ZIP_STORED) as wrxyut:
                    for root, dirs, files in os.walk('output/com.garena.game.kgth'):
                        for file in files:
                            file_path = os.path.join(root, file)
                            archive_file_path = os.path.relpath(file_path, 'output')
                            wrxyut.write(file_path, archive_file_path, compress_type=zipfile.ZIP_STORED)
                    try:
                        shutil.rmtree('output/com.garena.game.kgth')
                    except:
                        pass
    
            except Exception as e:
                print(Colorate.Color(Colors.red, f"[!] ERROR : {e}"))

    except KeyError:
        print(f"\n\n[!] ERROR: Could not find hero data for hero ID {heroId} and skin ID {SkinId}.\n\n")
        time.sleep(5)

    pause()
    main()

if __name__ == "__main__":
    main()

#    Saturn was proudly coded by wrxyut (https://github.com/wrxyut).
#    Copyright (c) 2022 wrxyut.
#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).