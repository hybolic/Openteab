from __future__ import annotations
import requests


try:from openteab.globals import *
except:import __init__; from openteab.globals import *

from openteab.main.config import RARE_BIOMES
from openteab.main.lib.macro_abstraction import MACRO_BASE
from openteab.globals import roblox, openteab
from openteab.main.lib.kbm_abstraction import MouseBase, KeyboardBase
from openteab.main.lib.screen_abstraction import PixelMode, ScreenBase
from openteab.main.lib.config import Config
from openteab.main.lib.variable_parse import *
from types import SimpleNamespace
from threading import Thread
import re, json

class BiomeCheck(MACRO_BASE):
    GITHUB_LOADED = False

    async def pre_loop(self, *args, **kwargs):
        raise NotImplementedError

    async def loop(self, *args, **kwargs):
        raise NotImplementedError

    async def post_loop(self, *args, **kwargs):
        raise NotImplementedError

    def loadConfig(self, raw_config = None):
        print_e("Loading Biome Check")
        print_e("Local Config, custom_biome_overrides")
        self.custom_biome_overrides = Config.getConfig().custom_biome_overrides
        print_e("Github Globals")
        self.Load_GithubDataURL()
        return
    
    def Load_GithubDataURL(self):
        if self.GITHUB_LOADED:
            return
        self.GITHUB_LOADED = True
        url      = openteab.biome_url
        eventUrl = openteab.biome_eventUrl

        default_biome_data = ParseToNamepsace(openteab.default_biome_data)

        try:
            r = requests.get(url, timeout=1)
            r.raise_for_status()
            data = r.json(object_hook=lambda d:SimpleNamespace(**d))
            if not isinstance(data, dict|SimpleNamespace) or not data:
                data = default_biome_data
        except Exception as e:
            print_e(e, f"Error loading biomes_data.json from {url}: {e}")
            data = default_biome_data

        try:
            r_events = requests.get(eventUrl, timeout=1)
            r_events.raise_for_status()
            events = r_events.json(object_hook=lambda d:SimpleNamespace(**d))
        except Exception as e:
            print_e(e, f"Error loading active_events.json from {eventUrl}: {e}")
            events.april_fools = False

        if events.april_fools:
            #TODO: change to month of april as fallback
            glitched = data.GLITCHED
            for biome in data:
                getattr(data, biome).color = glitched.get("color", getattr(data, biome).color)
                getattr(data, biome).thumbnail_url = glitched.get("thumbnail_url", getattr(data, biome).thumbnail_url)

        custom_overrides = self.custom_biome_overrides
        if isinstance(custom_overrides, SimpleNamespace):
            biome_list:dict = vars(custom_overrides).items()
            keylist = [*vars(custom_overrides).keys()]
            for biome_name, overrides in biome_list:
                try:
                    print_d(biome_name + " IS IN LIST? " + str(biome_name in keylist))
                    if biome_name in keylist and isinstance(overrides, SimpleNamespace):
                        biome = getattr(data, biome_name, None)
                        if hasattr(overrides, "color") and overrides.color:
                            biome.color = overrides.color
                        if hasattr(overrides, "thumbnail_url") and overrides.thumbnail_url:
                            biome.thumbnail_url = overrides.thumbnail_url
                        if hasattr(overrides, "start_description") and overrides.start_description:
                            biome.start_description = overrides.start_description
                        if hasattr(overrides, "end_description") and overrides.end_description:
                            biome.end_description = overrides.end_description
                except Exception as e:
                    print_e(f"problem while overriding defaults: {e}")
                    pass

        return data

    def _consume_log_username_validation(self, log_file_path, lines=None):
        try:
            try:
                #TODO: STRIP OUT CONFIG
                raw = self.config.get("roblox_username", "")
                if raw is None:
                    target_username = ""
                target_username = str(raw).strip().lower()
            except Exception:
                target_username = ""
            if not target_username:
                return True
            if not log_file_path:
                return False
            
            #TODO: INITIALISE STATE_MAP DURING INIT
            state_map = getattr(self, "_log_username_state_map", None)
            if not isinstance(state_map, dict):
                state_map = {}
                self._log_username_state_map = state_map
            
            #TODO: INITIALISE LAST_GUARD_USERNAME DURING INIT
            last_guard_username = getattr(self, "_log_username_state_target", None)
            if last_guard_username != target_username:
                state_map.clear()
                self._log_username_state_target = target_username

            state = state_map.get(log_file_path)
            if state == "rejected":
                return False
            if state == "accepted":
                return True
            if state is None:
                state_map[log_file_path] = "pending"

            # While this file is pending, keep scanning the entire file until
            # the TutorialCursor line appears and we can accept/reject it.
            lines_to_scan = lines
            if lines_to_scan is None:
                try:
                    with open(log_file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines_to_scan = f.readlines()
                except Exception:
                    lines_to_scan = []

            for line in (lines_to_scan or []):
                try:
                    if not line or "TutorialCursor" not in line or "Infinite yield possible" not in line or "Players." not in line:
                        found_username = ""
                    match = re.search(r"Players\.([^.']+)\.PlayerGui:WaitForChild\((?:\"|\\\")TutorialCursor(?:\"|\\\")\)", line, re.IGNORECASE)
                    if not match:
                        found_username = ""
                    found_username = str(match.group(1) or "").strip().lower()
                except Exception:
                    found_username = ""
                if not found_username:
                    continue
                if found_username == target_username:
                    state_map[log_file_path] = "accepted"
                    return True

                state_map[log_file_path] = "rejected"
                try:
                    print_i(
                        f"[Log Guard] Ignoring log file due to TutorialCursor username mismatch. "
                        f"Expected '{target_username}', got '{found_username}'."
                    )
                except Exception:
                    pass
                return False

            if len(state_map) > 200:
                state_map.clear()
                state_map[log_file_path] = "pending"
            return True
        except Exception as e:
            print_e(e, "Error validating log username guard")
            return True

    def read_log_file(self, log_file_path):
        if not path_exists(log_file_path):
            print_e(f"Log file not found: {log_file_path}")
            return []

        def is_chat_log(line):
            if "ExpChat" in line or "mountClientApp" in line or "Time record" in line or "[Server]" in line:
                excluded_phrases = [
                    "[Merchant]: Mari has arrived on the island...",
                    "[Merchant]: Jester has arrived on the island!!"
                ]
                return not any(phrase in line for phrase in excluded_phrases)
            return False

        if getattr(self, "_last_read_log_file_main", None) != log_file_path:
            self._last_read_log_file_main = log_file_path
            self.last_position = 0

        with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
            file.seek(self.last_position)
            lines = file.readlines()
            self.last_position = file.tell()
            if not self._consume_log_username_validation(log_file_path):
                return []
            return [line for line in lines if not is_chat_log(line)]
    
    def check_biome_in_logs(self):
        try:
            log_file_path = Roblox.get_latest_log_file()
            log_lines = self.read_log_file(log_file_path)
            for line in reversed(log_lines):
                            
                #TODO: implent C's Merchant Log Detection here
                #NOTE: if merchant and not at (last time of day)
                    #NOTE: send merchant update to merchant teleporter
                    #NOTE: if not teleporter then notify the player
                if "[BloxstrapRPC]" in line and '"largeImage"' in line:
                    match = re.search(r'"largeImage"\s*:\s*\{[^}]*"hoverText"\s*:\s*"([^"]+)"(?=,"assetId")(?:,"assetId":(\d+))', line)
                    if match:
                        biome = match.group(1).strip().upper()
                        
                        if biome not in self.biome_data:
                            print(f"New unlisted biome detected from RPC: {biome}")
                            try:
                                print(f"Auto-loaded new unlisted biome: {biome}")
                                asset_id = match.group(2)
                                png_path = openteab.images / f"biomes/{biome}-75.png"
                                if (not (png_path).exists()):
                                    if png_path.is_dir() and isinstance(png_path, Path):
                                        png_path.rmdir()
                                    asset_url = f"https://thumbnails.roblox.com/v1/assets?assetIds={asset_id}&size=75x75&format=Png"
                                    from urllib import request
                                    with request.urlopen(asset_url) as response:
                                        js = json.loads(response.read())
                                        if "data" in js and "imageUrl" in js["data"][0]:
                                            image_url = js["data"][0]["imageUrl"]
                                            request.urlretrieve(image_url, png_path)
                                            #TODO: move image into biome_data as either octal or b64 so it can be sent via packet to discord etc
                                            #TODO: once sent to discord request image url so we don't resend the image again after the first time
                                        else: raise Exception("NO DATA!")
                            except Exception as e: print_e(e)
                            
                            self.biome_data[biome] = {
                                "color": "0xffffff",
                                "thumbnail_url": openteab.biome_placeholder,
                                "encoded_thumbnail" : "",
                                "encoded_thumbnail_cached_url" : "" #NOTE: posibly reuse thumbnail url instead
                            }

                        if biome not in self.config["biome_notifier"] and biome not in RARE_BIOMES and biome != "NORMAL":
                            self.config["biome_notifier"][biome] = "Message"
                            try: 
                                self.save_config()
                            except Exception: pass

                        if biome != self.current_biome:
                            last_biome = self.current_biome
                            self.current_biome = biome
                            #TODO: change to simple webhook function and include biome_data[biome] object
                            #NOTE: this should remain a thread so it doesn't eat the main process but it should have a lock on it to prevent recalling
                            Thread(target=self.handle_biome_detection, args=(biome, last_biome)).start()
                            #TODO: send biome update to child Macros. ie, Autopop and Limbo
                        return

        except Exception as e:
            print_e(f"{e} Error in check_biome_in_logs function :skull:")
try:
    if DEBUG:
        raise NameError
    print_d("NO DEBUG")
except NameError:
    temp = BiomeCheck(None,None)
    temp.loadConfig()
    print_d("DONE")
