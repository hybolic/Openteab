from os import getcwd, makedirs, getenv
from os.path import join as join_path, exists as path_exists


class Roblox:
    logs = join_path(getenv("LOCALAPPDATA"), "Roblox", "logs")
    versions = join_path(getenv("LOCALAPPDATA"), "Roblox", "Versions")
roblox = Roblox()
class Openteab:
    cwd = getcwd()
    """ ./ """
    virtual_dir_name = ".python"

    def __init__(self):
        self.top_directory = join_path(self.cwd, "openteab")
        """ ./openteab """

        self.config_folder = join_path(self.cwd, "config_folder")
        """ ./config_folder """
        self.config_json = self._path(self.config_folder, "config.json")
        """ ./config_folder/config.json """

        self.venv = join_path(self.top_directory, self.virtual_dir_name)
        """ ./openteab/${virtual_dir_name} """
        self.venv_scripts = join_path(self.venv, "Scripts")
        """ ./openteab/${virtual_dir_name}/Scripts """

        self.python_exe = join_path(self.venv_scripts, "python.exe")
        """ ./openteab/${virtual_dir_name}/Scripts/python.exe """
        self.pip_exe = join_path(self.venv_scripts, "pip.exe")
        """ ./openteab/${virtual_dir_name}/Scripts/pip.exe """
        self.venv_activate_this = self._path(self.venv_scripts, "activate_this.py")
        self.venv_activate = join_path(self.venv_scripts, "activate")

        self.paths = self._path(self.top_directory, "paths")

        self.snowman_path = self._path(self.paths, "snowman.json")
        """ ./openteab/paths/snowman.json """
        self.obby_path = self._path(self.paths, "obby.json")
        """ ./openteab/paths/obby.json """
        self.crafting_files = self._path(self.top_directory, "crafting_files_do_not_open")
        """ ./openteab/crafting_files_do_not_open """
        self.assets = self._path(self.top_directory, "assets")
        """ ./openteab/assets """
        self.images = self._path(self.assets, "images")
        """ ./openteab/assets/images """
        self.screenshots = self._path(self.cwd, "screenshots")
        """ ./screenshots """
        self.frontend = self._path(self.top_directory, "frontend")
        """ ./openteab/frontend """

    @staticmethod
    def _path(path_start, path):
        path = join_path(path_start, path)
        if not path_exists(path):
            makedirs(path, exist_ok=True)
            print(f"Created paths folder: {path}")

        return path

    # ------------------------------------------------------------------
    # Requirements
    # ------------------------------------------------------------------

    requirements = ".\\requirements.txt"

    # ------------------------------------------------------------------
    # EasyOCR
    # ------------------------------------------------------------------

    class easyocr:
        image_url = "https://i.postimg.cc/FKtqPgBg/teleporter.png"
        ''' https://i.postimg.cc/FKtqPgBg/teleporter.png '''

        endpoints = [
            "https://cn-api.easyocr.org/ocr",
            "https://api.easyocr.org/ocr",
        ]
        ''' [ "https://cn-api.easyocr.org/ocr", "https://api.easyocr.org/ocr" ] '''

        api_url = endpoints[0]
        ''' endpoints[0] = "https://cn-api.easyocr.org/ocr" '''

    ##
    ## URLS / extra data
    ##

    # ------------------------------------------------------------------
    # Paths
    # ------------------------------------------------------------------

    snowman_path_url = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/paths/snowman.json"
    obby_path_url    = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/paths/obby.json"


    # ------------------------------------------------------------------
    # Notice / updates
    # ------------------------------------------------------------------

    notice_tab_contents_coteab   = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/noticetabcontents.txt"
    notice_tab_contents_openteab = "https://raw.githubusercontent.com/hybolic/OpenTeab/refs/heads/main/assets/noticetabcontents.txt"
    notice_tab_contents          = notice_tab_contents_coteab

    update_url_api_coteab  = "https://api.github.com/repos/xVapure/Noteab-Macro/releases/latest"
    update_url_api_opentab = "https://api.github.com/repos/hybolic/OpenTeab/releases/latest"
    update_url_api         = update_url_api_coteab
    update_url_coteab      = "https://github.com/xVapure/Noteab-Macro/releases/latest"
    update_url_opentab     = "https://github.com/hybolic/OpenTeab/releases/latest"
    update_url             = update_url_coteab

    coteab_discord = "https://discord.gg/fw6q274Nrt"

    # ------------------------------------------------------------------
    # Calibration
    # ------------------------------------------------------------------

    macro_calibration_youtube_long  = "https://www.youtube.com/watch?v=s2S7Bncx9ns"
    macro_calibration_youtube_short = "https://youtu.be/s2S7Bncx9ns"


    icon_url = "https://i.postimg.cc/rsXpGncL/Noteab-Biome-Tracker.png"


    # ------------------------------------------------------------------
    # Donations
    # ------------------------------------------------------------------

    class donations:
        link = "https://www.roblox.com/games/18203398779/Medival-castle#!/store"
        url = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/appreciation_list.txt"

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    event_url = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/main/active_events.json"

    event_link_rapidtables = "https://www.rapidtables.com/convert/color/index.html"


    # ------------------------------------------------------------------
    # Aura / merchant data
    # ------------------------------------------------------------------

    auras_json = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/auras.json"


    merchant_thumbnails = {
      "Mari": "https://i.postimg.cc/RZh2pw0j/mari.png",
      "Jester": "https://i.postimg.cc/7PBVsdTq/jester.png",
      "Rin": "https://i.postimg.cc/j5n9B6Km/rin.png"
    }

    eden_thumbnail = "https://raw.githubusercontent.com/vexthecoder/OysterDetector/refs/heads/main/eden.png"

    biome_url      = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/biomes_data.json"
    biome_eventUrl = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/active_events.json"

    default_biome_data = {
            "NORMAL": {
                "color": "0xffffff",
                "thumbnail_url": "no_url"
            },
            "WINDY": {
                "color": "0x9ae5ff",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/WINDY.png"
            },
            "RAINY": {
                "color": "0x027cbd",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/RAINY.png"
            },
            "SNOWY": {
                "color": "0xDceff9",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/SNOWY.png"
            },
            "SAND STORM": {
                "color": "0x8F7057",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/SAND%20STORM.png"
            },
            "HELL": {
                "color": "0xff4719",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/HELL.png"
            },
            "STARFALL": {
                "color": "0x011ab7",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/STARFALL.png"
            },
            "CORRUPTION": {
                "color": "0x6d32a8",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/CORRUPTION.png"
            },
            "NULL": {
                "color": "0x838383",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/NULL.png"
            },
            "GLITCHED": {
                "color": "0xbfff00",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/GLITCHED.png"
            },
            "DREAMSPACE": {
                "color": "0xea9dda",
                "thumbnail_url": "https://maxstellar.github.io/biome_thumb/DREAMSPACE.png"
            },
            "CYBERSPACE": {
                "color": "0x0A1A3D",
                "thumbnail_url": "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/images/CYBERSPACE.png"
            }
    }

openteab = Openteab()

def FROM_TOP(path):
    return openteab._path(openteab.cwd, path)

def FROM_PATH(path_start, path):
    return openteab._path(path_start, path)