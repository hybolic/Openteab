from os import getcwd, makedirs, getenv, getpid
from os.path import join as join_path, exists as path_exists
from win32gui import GetForegroundWindow, GetWindowText, GetWindowLong, IsWindowVisible, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId,GetWindowThreadProcessId
from psutil import Process, process_iter, TimeoutExpired, NoSuchProcess, AccessDenied, ZombieProcess
from ctypes import windll, byref, c_ulong
from win32con import GWL_STYLE, WS_CAPTION
from pygetwindow import getWindowsWithTitle, getAllTitles
from keyboard import press_and_release
from PIL import Image
from pyautogui import screenshot
from typing import Callable

class Roblox:
    def __init__(self):
        pass
    logs = join_path(getenv("LOCALAPPDATA"), "Roblox", "logs")
    versions = join_path(getenv("LOCALAPPDATA"), "Roblox", "Versions")
    
    def activate_roblox_window(self):
        hwnd = None
        try:
            hwnds = self._find_roblox_hwnds()
            if hwnds:
                hwnd = hwnds[0]
                self._focus_window_hwnd(hwnd, max_attempts=10, sleep_between=0.2)
        except Exception as e:
            print(f"[activate_roblox_window] hwnd path failed: {e}")

        if hwnd is None:
            # fallback
            try:
                for title in getAllTitles():
                    if "Roblox" in title:
                        win = getWindowsWithTitle(title)[0]
                        win.activate()
                        try:
                            hwnd = win._hWnd
                        except Exception:
                            pass
                        break
            except Exception as e:
                print(f"[activate_roblox_window] gw fallback failed: {e}")

        if hwnd is None:
            print("Roblox window not found.")
            return

        # Auto fullscreen
        if (
            self.config.get("auto_roblox_fullscreen", False)
            and not getattr(self, "_roblox_fullscreened", False)
        ):
            try:
                style = GetWindowLong(hwnd, GWL_STYLE)
                has_caption = bool(style & WS_CAPTION)
                if has_caption:
                    time.sleep(0.5)
                    fg = GetForegroundWindow()
                    if fg == hwnd:
                        press_and_release("f11")
                        time.sleep(0.3)
                        self.append_log("[Roblox] Roblox is now on fullscreen.")
                    else:
                        self.append_log("[Roblox] Roblox is not in foreground.")
                self._roblox_fullscreened = True
            except Exception as e:
                print(f"[activate_roblox_window] fullscreen failed: {e}")

    def _find_roblox_hwnds(self):
        pids = set()
        try:
            current_user = Process().username()
            current_user_norm = str(current_user or "").strip().lower()
        except Exception:
            current_user = None
            current_user_norm = ""
        try:
            for proc in process_iter(['pid', 'name', 'username']):
                try:
                    proc_name = str(proc.info.get('name') or "")
                    if proc_name not in ['RobloxPlayerBeta.exe', 'Windows10Universal.exe']:
                        continue

                    proc_user_norm = str(proc.info.get('username') or "").strip().lower()
                    if current_user is not None and current_user_norm and proc_user_norm and proc_user_norm != current_user_norm:
                        continue

                    pid = proc.info.get('pid')
                    if pid is not None:
                        pids.add(pid)
                except Exception:
                    pass
        except Exception:
            pass

        hwnds = []
        try:
            def enum_cb(hwnd, lparam):
                try:
                    if not IsWindowVisible(hwnd) or not IsWindowEnabled(hwnd):
                        return True
                    tid, pid = GetWindowThreadProcessId(hwnd)
                    if pid in pids:
                        hwnds.append(hwnd)
                except Exception:
                    pass
                return True

            EnumWindows(enum_cb, None)
        except Exception:
            pass
        return hwnds

    def is_roblox_focused(self):
        kernel32 = windll.kernel32
        try:
            hwnd = GetForegroundWindow()
            if not hwnd: return False
            try:
                _, fg_pid = GetWindowThreadProcessId(hwnd)
                if fg_pid:
                    my_session = c_ulong()
                    kernel32.ProcessIdToSessionId(getpid(), byref(my_session))
                    their_session = c_ulong()
                    kernel32.ProcessIdToSessionId(fg_pid, byref(their_session))
                    if my_session.value != their_session.value: return False
            except Exception: pass
            title = (GetWindowText(hwnd) or "").lower()
            if "roblox" in title: return True
            try:
                _, pid = GetWindowThreadProcessId(hwnd)
                if pid:
                    proc = Process(pid)
                    pname = (proc.name() or "").lower()
                    if "roblox" in pname: return True
            except Exception: pass
            return False
        except Exception: return False

    def check_roblox_procs(self):
        try:
            current_user = Process().username()
            current_user_norm = str(current_user or "").strip().lower()
            running_processes = process_iter(['pid', 'name', 'username'])
            roblox_processes = []

            for proc in running_processes:
                proc_name = str(proc.info.get('name') or "")
                if proc_name not in ['RobloxPlayerBeta.exe', 'Windows10Universal.exe']:
                    continue

                proc_user_norm = str(proc.info.get('username') or "").strip().lower()
                if current_user_norm and proc_user_norm and proc_user_norm != current_user_norm:
                    continue

                roblox_processes.append(proc.info)

            if roblox_processes:
                try:
                    hwnds = self._find_roblox_hwnds()
                    if not hwnds: return False
                except Exception: pass
                return True

        except Exception as e:
            print(e, "Error in check_roblox_procs function.")

        return False  # no Roblox processes are found

    def terminate_roblox_processes(self):
        try:
            current_user = Process().username()
            current_user_norm = str(current_user or "").strip().lower()
            running_processes = process_iter(['pid', 'name', 'username'])
            target_procs = ['RobloxPlayerBeta.exe', 'Windows10Universal.exe', 'RobloxPlayerLauncher.exe', 'RobloxCrashHandler.exe']

            for proc in running_processes:
                try:
                    proc_info = proc.info
                    proc_name = str(proc_info.get('name') or "")
                    if proc_name not in target_procs: continue
                    proc_user_norm = str(proc_info.get('username') or "").strip().lower()
                    if current_user_norm and proc_user_norm and proc_user_norm != current_user_norm: continue
                    print(f"Terminating process: {proc_name} (PID: {proc_info.get('pid')})")
                    try:
                        proc.kill()
                        proc.wait(timeout=3)
                    except TimeoutExpired:
                        pass
                except (NoSuchProcess, AccessDenied, ZombieProcess):
                    pass

        except Exception as e:
            print(e, "Error in terminate_roblox_processes function.")


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
        makedirs(self.screenshots, exist_ok=True)
        """ ./screenshots """
        self.frontend = self._path(self.top_directory, "frontend")
        """ ./openteab/frontend """
        self.frontend_public = self._path(self.frontend, "public")
        """ ./openteab/frontend/public """
        self.icon_path       = self._path(self.frontend_public, "NoteabBiomeTracker.ico")
        """ ./openteab/frontend/public/NoteabBiomeTracker.ico """

    @staticmethod
    def _path(path_start, path):
        path = join_path(path_start, path)
        if not path_exists(path):
            makedirs(path, exist_ok=True)
            print(f"Created paths folder: {path}")

        return path
    
    def save_screenshot(File:str, Webhook:Callable|None=None, Area:tuple[int, int, int, int]|None=None, *args, **kwargs):
        path = join_path(openteab.screenshots, File)
        if not roblox.is_roblox_focused():
            print("Roblox not focused, skipping screenshot", type="Screenshot")
            return None
        else:
            img = screenshot(Area)
            img.save(path)
            print(f"Saved to: {path}, exists: {path_exists(path)}")
        if Webhook is not None:
            try:
                Webhook(*args, **kwargs, screenshot_path=path)
            except Exception as e:
                from inspect import currentframe
                def namestr(obj, namespace):
                    return [name for name in namespace if namespace[name] is obj]
                def names_in_caller(obj, depth=2) -> list[str]:
                    frame = currentframe()
                    for _ in range(depth):
                        if frame is None:
                            return []
                        frame = frame.f_back
                    if frame is None:
                        return []
                    return namestr(obj, frame.f_locals)
                hook_name = names_in_caller(Webhook)
                print(f"Failed to send {hook_name}: {e}", (args, kwargs), type="webhook")

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

    path_url         = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/paths/"
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


    icon_url  = "https://i.postimg.cc/rsXpGncL/Noteab-Biome-Tracker.png"

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

    eden_thumbnail = "https://i.postimg.cc/q7jFZVMp/eden.png"
    egg_thumbnail  = "https://i.postimg.cc/FzRsHF7y/eggdoggo.png"
    biome_url      = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/biomes_data.json"
    biome_eventUrl = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/assets/active_events.json"
    biome_placeholder = "https://raw.githubusercontent.com/xVapure/Noteab-Macro/refs/heads/main/images/biome_placeholder.png"
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