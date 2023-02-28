
import os, zipfile, shutil
import xml.etree.ElementTree as ET
from utils.Zstd import ZstdStart
from utils.plugins.common import *
from pystyle import Colorate, Colors, Center

#    Saturn was proudly coded by wrxyut (https://github.com/wrxyut).
#    Copyright (c) 2022 wrxyut.
#    Saturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).

class Ages:
    def __init__(self, version, assets_dir, output_dir, parent_dir, ages, heroId, SkinId, NAME_CASE1, NAME_CASE2, ReturnCityEffect) -> None:
        self.version = version
        self.assets_dir = assets_dir
        self.output_dir = output_dir
        self.parent_dir = parent_dir
        self.ages = ages
        self.heroId = heroId
        self.SkinId = SkinId
        self.NAME_CASE1 = NAME_CASE1
        self.NAME_CASE2 = NAME_CASE2
        self.ReturnCityEffect = ReturnCityEffect

    # Method to get the file path of a package of Actions related to a hero
    def getActionsBytes(self):
        # Return the file path constructed using the assets_dir and ages attributes
        return f'{self.assets_dir}/{self.ages}/Actor_{self.heroId}_Actions.pkg.bytes'

    # Method to get the directory path of the skill files
    def getActionsDir(self):
        # Return the directory path constructed using the output_dir, parent_dir, and ages attributes
        return f'{self.output_dir}/{self.parent_dir}/{self.ages}/{self.NAME_CASE2}/skill'

    # Method to get the path of the CommonActions directory
    def getCommonActionsDir(self):
        return f'assets/{self.ages}/CommonActions.pkg.bytes'

    # Method to extract files from a given path
    def FileExtractor(self, FileExtractorPath, heroId=None):
        
        # If the file being extracted is the Actions file for a hero
        if os.path.basename(FileExtractorPath) == f"Actor_{heroId}_Actions.pkg.bytes":
            with zipfile.ZipFile(FileExtractorPath, "r") as Extract:
            
                # Extract the contents to the specified ages directory
                Extract.extractall(f'{self.output_dir}/{self.parent_dir}/{self.ages}')
        
        # If the basename of the file path to extract is "CommonActions.pkg.bytes".
        if os.path.basename(FileExtractorPath) == "CommonActions.pkg.bytes":

            # Define the target directory for the extracted files.
            commonresource = os.path.join('assets', 'ReturnCityEffect')

            # Open the "CommonActions.pkg.bytes" file for reading and extracting its contents.
            with zipfile.ZipFile(self.getCommonActionsDir(), "r") as Extract:

                # If the target directory does not exist, create it.
                if not os.path.exists(commonresource):
                    os.makedirs(commonresource)

                # Extract all the contents of the ZIP archive to the target directory.
                Extract.extractall(commonresource)

    def bAllowEmptyEffect(self, SkinId, NAME_CASE2):

        for file_name in os.listdir(os.path.join(self.output_dir, self.parent_dir, self.ages, NAME_CASE2, 'skill')):
            file_path = os.path.join(self.output_dir, self.parent_dir, self.ages, NAME_CASE2, 'skill', file_name)
        
            try:
                tree = ET.parse(file_path)
            except ET.ParseError:
                continue
        
            root = tree.getroot()
        
            special_effect = root.findall(f".//Track[@trackName='{SkinId}']/Event[@eventName='CheckSkinIdTick']/int[@name='skinId']")
            for string_element in special_effect:
                string_element.attrib['value'] = f'{SkinId[:-2]}00'
            tree.write(file_path, encoding="utf-8", xml_declaration=True)

            bAllowEmptyEffect = root.findall(".//bool[@name='bAllowEmptyEffect']")
            for string_element in bAllowEmptyEffect:
                string_element.attrib['value'] = 'false'
            
            tree.write(file_path, encoding="utf-8", xml_declaration=True)


    def do_ages(self):
        setTitle(f"Ages (Actor_{self.heroId}_Actions.pkg.bytes) Modifying")
        
        try:

            self.FileExtractor(self.getActionsBytes(), self.heroId)

            # Start a Zstd process to decompress the XML file.
            ZstdStart(self.getActionsDir())

            Sound_suffix = str(self.SkinId[3:]) if int(self.SkinId[3:]) >= 10 else str(self.SkinId[4:])

            for file_name in os.listdir(self.getActionsDir()):
                file_path = os.path.join(self.getActionsDir(), file_name)

                if "Back" in file_path:
                    continue
                
                try:
                    tree = ET.parse(file_path)
                except ET.ParseError:
                    continue


                root = tree.getroot()

                TriggerParticle_elm = root.findall(".//Event[@eventName='TriggerParticle']/String[@name='resourceName']")
                TriggerParticleTick_elm = root.findall(".//Event[@eventName='TriggerParticleTick']/String[@name='resourceName']")
                PlayHeroSoundTick_elm = root.findall(".//Event[@eventName='PlayHeroSoundTick']/String[@name='eventName']")

                if len(TriggerParticleTick_elm) == 0 and len(TriggerParticle_elm) == 0 and len(PlayHeroSoundTick_elm) == 0:
                    continue
                
                for string_element in (TriggerParticleTick_elm + TriggerParticle_elm):

                    old_value = string_element.attrib['value']

                    if not old_value:
                        continue

                    if self.SkinId in old_value:
                        continue
                    
                    # If the heroId followed by the string "NAME_CASE1" is in the old value, 
                    # replace it with the heroId followed by "NAME_CASE1" and the skinId separated by a slash
                    if str(self.heroId + self.NAME_CASE1) in old_value:
                        new_value = old_value.replace(str(self.heroId + self.NAME_CASE1), f"{str(self.heroId + self.NAME_CASE1)}/{self.SkinId}")
                        string_element.attrib['value'] = new_value
                        wrxyut27 = f"{str(self.heroId + self.NAME_CASE1)}/{self.SkinId}"

                    # If the string "NAME_CASE2" is in the old value, 
                    # replace it with "NAME_CASE2" and the skinId separated by a slash
                    elif str(self.NAME_CASE2) in old_value:
                        new_value = old_value.replace(str(self.NAME_CASE2), f"{str(self.NAME_CASE2)}/{self.SkinId}")
                        string_element.attrib['value'] = new_value
                        wrxyut27 = f"{str(self.NAME_CASE2)}/{self.SkinId}"

                for string_element in PlayHeroSoundTick_elm:

                    old_value = string_element.attrib['value']

                    if not old_value:
                        continue

                    # Append the string '_Skin' followed by the Sound_suffix to the old value
                    new_value = old_value + f'_Skin{Sound_suffix}'

                    string_element.attrib['value'] = new_value

                # Write the modified XML tree back to the original file path with UTF-8 encoding and an XML declaration
                tree.write(file_path, encoding="utf-8", xml_declaration=True)


            # bAllowEmptyEffect
            if self.SkinId == "11614" or "15009" or "14111" or "54402":
                self.bAllowEmptyEffect(self.SkinId, self.NAME_CASE2)


            # Start a Zstd process to compress the XML file.
            ZstdStart(self.getActionsDir())

            with zipfile.ZipFile(os.path.join(self.output_dir, self.parent_dir, self.ages, f'Actor_{self.heroId}_Actions.pkg.bytes'), 'w', compression=zipfile.ZIP_STORED) as actions_pkg:
                
                for root, dirs, files in os.walk(os.path.join(self.output_dir, self.parent_dir, self.ages, self.NAME_CASE2)):
                    for file in files:
                        file_path = os.path.join(root, file)
                        archive_file_path = os.path.relpath(file_path, 
                                                            os.path.join(os.path.join(self.output_dir, 
                                                                                    self.parent_dir, 
                                                                                    self.ages, 
                                                                                    self.NAME_CASE2), 
                                                                                    '..'))
                        
                        actions_pkg.write(file_path, archive_file_path, compress_type=zipfile.ZIP_STORED)
            try:
                shutil.rmtree(os.path.join(self.output_dir, 
                                        self.parent_dir, 
                                        self.ages, 
                                        self.NAME_CASE2))
            except:
                pass

            print(Colorate.Horizontal(Colors.yellow_to_red, f"[+] Actor_{self.heroId}_Actions.pkg.bytes Modify successfully."))
        except Exception as e:
            print(Colorate.Color(Colors.red, f"[!] ERROR : {e}"))


        if self.ReturnCityEffect.lower() == "y":
            setTitle(f"Ages (CommonActions.pkg.bytes) Modifying")
            try:

                self.FileExtractor(self.getCommonActionsDir())

                # Start a Zstd process to decompress the XML file.
                ZstdStart(os.path.join('assets', 'ReturnCityEffect', 'commonresource', 'Back.xml'))


                back_path = os.path.join('assets', 'ReturnCityEffect', 'commonresource', 'Back.xml')

                try:
                    tree = ET.parse(back_path)
                except ET.ParseError:
                    pass

                root = tree.getroot()

                # Find all `Track` elements with attribute `trackName` set to '544', 
                # and update their `trackName` attribute to `heroId`.
                tracks = root.findall(".//Track[@trackName='544']")
                for track in tracks:
                    track.attrib['trackName'] = self.heroId
                
                # Find all `Track` elements with attribute `guid` set to '544', 
                # and update their `guid` attribute to `heroId`.
                guid0 = root.findall(".//Track[@guid='544']")
                for guid in guid0:
                    guid.attrib['guid'] = self.heroId

                # Find all `Event` elements with attribute `eventName` set to 'CheckHeroIdTick', 
                # and update their `guid` attribute and the `value` attribute of their child `int` element to `heroId`.
                check_hero_id_tick = root.findall(".//Event[@eventName='CheckHeroIdTick']")
                for event in check_hero_id_tick:
                    event.attrib['guid'] = self.heroId
                    int_element = event.find(".//int[@name='heroId']")
                    int_element.attrib['value'] = self.heroId

                # Find all `Condition` elements, and update their `guid` attribute to `heroId`.
                conditions = root.findall(".//Condition")
                for condition in conditions:
                    condition.attrib['guid'] = self.heroId

                # Find all `Event` elements with attribute `eventName` set to 'GetHolidayResourcePathTick', 
                # and update the `value` attribute of their child `String` element with the attribute `name` 
                # set to `'holidayResourcePathPrefix'` if it does not match certain values.
                holiday_resource_path_tick = root.findall(".//Event[@eventName='GetHolidayResourcePathTick']")
                for event in holiday_resource_path_tick:
                    string_element = event.find(".//String[@name='holidayResourcePathPrefix']")
                    old_value = string_element.attrib['value']
                    if old_value != 'Prefab_Skill_Effects/Inner_Game_Effect/returncity_holidays/Holiday0/huijidi' and old_value != 'Prefab_Skill_Effects/Inner_Game_Effect/returncity_holidays/Holiday0/huicheng_tongyong':
                        string_element.attrib['value'] = old_value.replace('544_Painter/54402', wrxyut27)

                # Write the modified XML tree back to the original file path with UTF-8 encoding and an XML declaration
                tree.write(back_path, encoding="utf-8", xml_declaration=True)
                
                # Append a credit message to the end of the XML file.
                with open(back_path, 'a') as credit:
                    credit.write("\n\n\n<!--\nSaturn was proudly coded by wrxyut (https://github.com/wrxyut).")
                    credit.write("\nCopyright (c) 2022 wrxyut")
                    credit.write("\nSaturn under the GNU GENERAL PUBLIC LICENSE Version3 (2007).\n-->")

                # Start a Zstd process to compress the XML file.
                ZstdStart(os.path.join('assets', 'ReturnCityEffect', 'commonresource', 'Back.xml'))

                # Create a ZIP file and write compressed data to it.
                with zipfile.ZipFile(os.path.join(f"{self.output_dir}/{self.parent_dir}/{self.ages}/CommonActions.pkg.bytes"), 'w', compression=zipfile.ZIP_STORED) as wrxyut:
                    
                    len_dir = len(os.path.join('assets', 'ReturnCityEffect'))

                    for root, _, files in os.walk(os.path.join('assets', 'ReturnCityEffect')):
                        for file in files:
                            file_path = os.path.join(root, file)

                            wrxyut.write(file_path, file_path[len_dir:], compress_type=zipfile.ZIP_STORED)
                    
                    try:
                        shutil.rmtree(os.path.join('assets', 'ReturnCityEffect'))
                    except:
                        pass
            
                print(Colorate.Horizontal(Colors.yellow_to_red, f"[+] CommonActions.pkg.bytes Modify successfully."))
            except Exception as e:
                print(Colorate.Color(Colors.red, f"[!] ERROR : {e}"))