
import os, zipfile
from utils.Zstd import ZstdStart
from utils.version import getVersion
from utils.plugins.common import *

#    Saturn was proudly coded by wrxyut (https://github.com/wrxyut).
#    Copyright (c) 2022 wrxyut.
#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).

class Databin:
    def __init__(self, assets_dir, output_dir, parent_dir, databin, heroId, SkinId) -> None:
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.parent_dir = parent_dir
        self.databin = databin
        self.heroId = heroId
        self.SkinId = SkinId

    # Method to extract files from a given path
    def FileExtractor(self, FileExtractorPath):
        if os.path.basename(FileExtractorPath) == "Sound.zip" or "Actor.zip" or "Shop.zip":
            with zipfile.ZipFile(FileExtractorPath, "r") as Extractor:
                Extractor.extractall(f'{self.output_dir}/{self.parent_dir}/{self.databin}')


    # Databin/Sound
    @staticmethod
    def sound_format(skinId):
        bytes_code = hex(int(skinId))[2:]
        return bytes_code[2:] + bytes_code[:2]
    
    def do_sound(self, heroId_format, SkinId_format):
        setTitle("Databin (Sound) Modifying")

        try:
            self.FileExtractor(f"assets/{self.databin}/Sound.zip")
            sound_path = f"{self.output_dir}/{self.parent_dir}/{self.databin}/Sound"

            # Start a Zstd process to decompress the Bytes file.
            ZstdStart(sound_path)

            for file_name in os.listdir(sound_path):
                file_path = os.path.join(sound_path, file_name)

                with open(file_path, "rb") as f:
                    sound_file = f.read()
                    sound_file = sound_file.hex().\
                    replace(heroId_format, "0000").\
                    replace(SkinId_format, heroId_format)
                    sound_file = bytes.fromhex(sound_file)

                with open(file_path, "wb") as f:
                    f.write(sound_file)

            # Start a Zstd process to compress the Bytes file.
            ZstdStart(sound_path)
            
            print(Colorate.Horizontal(Colors.yellow_to_red, "[+] Sound modify successfully."))
        except Exception as e:
            print(Colorate.Color(Colors.red, f"[!] ERROR : {e}"))


