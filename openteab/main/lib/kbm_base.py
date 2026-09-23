from __future__ import annotations
from typing import Any, get_args, Literal, Final

DIRECTION = Literal['UP','DOWN']

from abc import ABC, abstractmethod

KeyMapType = dict[str, tuple[list[str], list[str]]]
KeyMapMode = Literal["AUTOIT","AHK"] 
"""Current Valid KeyMapNames, check Dict KeyMapDict"""

STANDARD_AUTOIT:Final[KeyMapType] = {
    # --- Modifiers (Individual & Combined) ---
    "^!+": ["{CTRL}{ALT}{SHIFT}", "ctrl+alt+shift"],
    "^!":  ["{CTRL}{ALT}", "ctrl+alt"],
    "^+":  ["{CTRL}{SHIFT}", "ctrl+shift"],
    "!+":  ["{ALT}{SHIFT}", "alt+shift"],
    "^":   ["{CTRL}", "ctrl"],
    "!":   ["{ALT}", "alt"],
    "+":   ["{SHIFT}", "shift"],
    "#":   ["{WIN}", "win"],  # AutoIt uses # for Windows key

    # --- Directional Modifiers ---
    "{LCTRL}":  ["{LCTRL}", "left ctrl"],
    "{RCTRL}":  ["{RCTRL}", "right ctrl"],
    "{LALT}":   ["{LALT}", "left alt"],
    "{RALT}":   ["{RALT}", "right alt"],
    "{LSHIFT}": ["{LSHIFT}", "left shift"],
    "{RSHIFT}": ["{RSHIFT}", "right shift"],
    "{LWIN}":   ["{LWIN}", "left win"],
    "{RWIN}":   ["{RWIN}", "right win"],

    # --- Standard Keys & Navigation ---
    "{ENTER}":     ["{ENTER}", "enter"],
    "{ALTTAB}":    ["{ALTTAB}", "alt+tab"],
    "{BACKSPACE}": ["{BACKSPACE}", "backspace"],
    "{BS}":        ["{BS}", "backspace"],
    "{DELETE}":    ["{DELETE}", "delete"],
    "{DEL}":       ["{DEL}", "delete"],
    "{UP}":        ["{UP}", "up"],
    "{DOWN}":      ["{DOWN}", "down"],
    "{LEFT}":      ["{LEFT}", "left"],
    "{RIGHT}":     ["{RIGHT}", "right"],
    "{HOME}":      ["{HOME}", "home"],
    "{END}":       ["{END}", "end"],
    "{ESCAPE}":    ["{ESCAPE}", "esc"],
    "{ESC}":       ["{ESC}", "esc"],
    "{INSERT}":    ["{INSERT}", "insert"],
    "{INS}":       ["{INS}", "insert"],
    "{PGUP}":      ["{PGUP}", "page up"],
    "{PGDN}":      ["{PGDN}", "page down"],
    "{TAB}":       ["{TAB}", "tab"],
    "{SPACE}":     ["{SPACE}", "space"],
    "{PRINTSCREEN}":["{PRINTSCREEN}", "print screen"],
    "{CAPSLOCK}":  ["{CAPSLOCK}", "caps lock"],

    # --- Numpad Keys ---
    "{NUMPAD0}":     ["{NUMPAD0}", "num 0"],
    "{NUMPAD1}":     ["{NUMPAD1}", "num 1"],
    "{NUMPAD2}":     ["{NUMPAD2}", "num 2"],
    "{NUMPAD3}":     ["{NUMPAD3}", "num 3"],
    "{NUMPAD4}":     ["{NUMPAD4}", "num 4"],
    "{NUMPAD5}":     ["{NUMPAD5}", "num 5"],
    "{NUMPAD6}":     ["{NUMPAD6}", "num 6"],
    "{NUMPAD7}":     ["{NUMPAD7}", "num 7"],
    "{NUMPAD8}":     ["{NUMPAD8}", "num 8"],
    "{NUMPAD9}":     ["{NUMPAD9}", "num 9"],
    "{NUMPADENTER}": ["{NUMPADENTER}", "num enter"],
    "{NUMPADADD}":   ["{NUMPADADD}", "num +"],
    "{NUMPADSUB}":   ["{NUMPADSUB}", "num -"],
    "{NUMPADMULT}":  ["{NUMPADMULT}", "num *"],
    "{NUMPADDIV}":   ["{NUMPADDIV}", "num /"],
    "{NUMPADDOT}":   ["{NUMPADDOT}", "num ."],

    # --- Function Keys ---
    "{F1}":  ["{F1}", "f1"],
    "{F2}":  ["{F2}", "f2"],
    "{F3}":  ["{F3}", "f3"],
    "{F4}":  ["{F4}", "f4"],
    "{F5}":  ["{F5}", "f5"],
    "{F6}":  ["{F6}", "f6"],
    "{F7}":  ["{F7}", "f7"],
    "{F8}":  ["{F8}", "f8"],
    "{F9}":  ["{F9}", "f9"],
    "{F10}": ["{F10}", "f10"],
    "{F11}": ["{F11}", "f11"],
    "{F12}": ["{F12}", "f12"],

    # --- AutoIt Escaped Special Characters ---
    "{{}": ["{"],
    "{}}": ["}"],
    "{!}": ["!"],
    "{#}": ["#"],
    "{+}": ["+"],
    "{^}": ["^"],
}
STANDARD_AHK:Final[KeyMapType] = {
    # --- AltGr & Special Combinations ---
    "<^>!": ["{LCTRLDOWN}{RALT}{LCTRLUP}", "left ctrl+right alt"],  # AltGr

    # --- Positional Modifiers ---
    "<!": ["{LALT}", "left alt"],
    ">!": ["{RALT}", "right alt"],
    "!":  ["{ALT}", "alt"],
    "<+": ["{LSHIFT}", "left shift"],
    ">+": ["{RSHIFT}", "right shift"],
    "+":  ["{SHIFT}", "shift"],
    "<^": ["{LCTRL}", "left ctrl"],
    ">^": ["{RCTRL}", "right ctrl"],
    "^":  ["{CTRL}", "ctrl"],
    "<#": ["{LWIN}", "left win"],
    ">#": ["{RWIN}", "right win"],
    "#":  ["{WIN}", "win"],

    # --- Standard Keys & Navigation ---
    "{ENTER}":     ["{ENTER}", "enter"],
    "{BACKSPACE}": ["{BACKSPACE}", "backspace"],
    "{BS}":        ["{BS}", "backspace"],
    "{DELETE}":    ["{DELETE}", "delete"],
    "{DEL}":       ["{DEL}", "delete"],
    "{UP}":        ["{UP}", "up"],
    "{DOWN}":      ["{DOWN}", "down"],
    "{LEFT}":      ["{LEFT}", "left"],
    "{RIGHT}":     ["{RIGHT}", "right"],
    "{HOME}":      ["{HOME}", "home"],
    "{END}":       ["{END}", "end"],
    "{ESCAPE}":    ["{ESCAPE}", "esc"],
    "{ESC}":       ["{ESC}", "esc"],
    "{INSERT}":    ["{INSERT}", "insert"],
    "{INS}":       ["{INS}", "insert"],
    "{PGUP}":      ["{PGUP}", "page up"],
    "{PGDN}":      ["{PGDN}", "page down"],
    "{TAB}":       ["{TAB}", "tab"],
    "{SPACE}":     ["{SPACE}", "space"],
    "{PRINTSCREEN}":["{PRINTSCREEN}", "print screen"],
    "{CAPSLOCK}":  ["{CAPSLOCK}", "caps lock"],
    "{APPSKEY}":   ["{APPSKEY}", "menu"],

    # --- Numpad Keys ---
    "{Numpad0}":      ["{Numpad0}", "num 0"],
    "{Numpad1}":      ["{Numpad1}", "num 1"],
    "{Numpad2}":      ["{Numpad2}", "num 2"],
    "{Numpad3}":      ["{Numpad3}", "num 3"],
    "{Numpad4}":      ["{Numpad4}", "num 4"],
    "{Numpad5}":      ["{Numpad5}", "num 5"],
    "{Numpad6}":      ["{Numpad6}", "num 6"],
    "{Numpad7}":      ["{Numpad7}", "num 7"],
    "{Numpad8}":      ["{Numpad8}", "num 8"],
    "{Numpad9}":      ["{Numpad9}", "num 9"],
    "{NumpadDot}":    ["{NumpadDot}", "num ."],
    "{NumpadDiv}":    ["{NumpadDiv}", "num /"],
    "{NumpadMult}":   ["{NumpadMult}", "num *"],
    "{NumpadSub}":    ["{NumpadSub}", "num -"],
    "{NumpadAdd}":    ["{NumpadAdd}", "num +"],
    "{NumpadEnter}":  ["{NumpadEnter}", "num enter"],

    # --- Function Keys ---
    "{F1}":  ["{F1}", "f1"],
    "{F2}":  ["{F2}", "f2"],
    "{F3}":  ["{F3}", "f3"],
    "{F4}":  ["{F4}", "f4"],
    "{F5}":  ["{F5}", "f5"],
    "{F6}":  ["{F6}", "f6"],
    "{F7}":  ["{F7}", "f7"],
    "{F8}":  ["{F8}", "f8"],
    "{F9}":  ["{F9}", "f9"],
    "{F10}": ["{F10}", "f10"],
    "{F11}": ["{F11}", "f11"],
    "{F12}": ["{F12}", "f12"],

    # --- AHK Raw/Escaped Symbols ---
    "`{": ["{"],
    "`}": ["}"],
    "`!": ["!"],
    "`#": ["#"],
    "`+": ["+"],
    "`^": ["^"],
    "``": ["`"],
}

INTDEFAULT:Literal[0] = 0
SPEED_DEFAULT:Literal[-1] = -1
CLICK_DEFAULT:Literal[1] = 1

KeyMapDict = {"AUTOIT":STANDARD_AUTOIT,"AHK":STANDARD_AHK}
"""dictionary of keymaps"""

class KeyboardBase(ABC):
    CURRENT_INSTANCE:KeyboardBase=...
    __CURRENT_MODE:KeyMapMode="AUTOIT"

    @staticmethod
    @property
    def CURRENT_MODE() -> KeyMapMode:
        """current mapping name for send"""
        return KeyboardBase.__CURRENT_MODE
    
    @staticmethod
    @property
    def CURRENT() -> KeyMapType:
        """current mapping for send"""
        return KeyMapDict[KeyboardBase.__CURRENT_MODE]
    
    @staticmethod
    def SetMode(MODE:KeyMapMode):
        if MODE not in get_args(KeyMapMode):
            raise TypeError(f"Invalid Keymap {MODE}")
        KeyboardBase.__CURRENT_MODE = MODE

    @staticmethod
    @abstractmethod
    def setClipboard(text):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def getClipboard():
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def press(key):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def release(key):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_pressed(key):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def key_to_scan_codes(key, error_if_missing=True):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def is_modifier(key):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def send(send_text:str, mode:int|bool=0):
        """
        Sends simulated keystrokes to the active window.

        Args:
            send_text (str): text.
            mode (int): Changes how "keys" is processed:
                flag = 0 (default): Text contains special characters like "+" and "!"
                                    to indicate SHIFT and ALT key presses.
                flag = 1: keys are sent raw.
        for string based special characters
            see here: https://www.autohotkey.com/docs/v1/Hotkeys.htm
        """
        raise NotImplementedError

    
    @classmethod
    def setAHKMode(cls):...

    @classmethod
    def setAutoItMode(cls):...

    @staticmethod
    def quickPasteText(text):
        old_clipboard = KeyboardBase.CURRENT_INSTANCE.getClipboard()
        KeyboardBase.CURRENT_INSTANCE.setClipboard(text)
        KeyboardBase.CURRENT_INSTANCE.send("{CTRL}v",0)
        KeyboardBase.CURRENT_INSTANCE.setClipboard(old_clipboard)

class Mouse:
    """storage for mouse buttons"""
    class Button(str):pass
    LEFT   =Button("left")
    RIGHT  =Button("right")
    MIDDLE =Button("middle")
    BUTTON4=Button("")
    BUTTON5=Button("")

class MouseBase(ABC):

    @staticmethod
    @abstractmethod
    def mouse_click(button:Mouse.Button|str=Mouse.LEFT, x:int=INTDEFAULT, y:int=INTDEFAULT, clicks:int=CLICK_DEFAULT, speed:int=SPEED_DEFAULT) -> Any|None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mouse_click_drag(x1:int, y1:int, x2:int, y2:int, button:Mouse.Button|str=Mouse.LEFT, speed:int=SPEED_DEFAULT) -> Any|None:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def mouse_down(button:Mouse.Button|str=Mouse.LEFT) -> Any|None:
        raise NotImplementedError
    
    @staticmethod
    @abstractmethod
    def mouse_up(button:Mouse.Button|str=Mouse.LEFT) -> Any|None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mouse_get_pos() -> tuple[int, int]:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def mouse_move(x:int, y:int, speed:int=SPEED_DEFAULT) -> Any|None:
        raise NotImplementedError


    """MOUSE WHEEL IMPLMENTATION"""
    @staticmethod
    @abstractmethod
    def mouse_wheel(direction:DIRECTION|str, clicks:int=CLICK_DEFAULT) -> Any|None:
        raise NotImplementedError

    @classmethod
    def mouse_wheel_up(cls,clicks:int=CLICK_DEFAULT) -> Any|None:
        return cls.mouse_wheel("UP",clicks)

    @classmethod
    def mouse_wheel_down(cls,clicks:int=CLICK_DEFAULT) -> Any|None:
        return cls.mouse_wheel("DOWN",clicks)


try:
    from typing import List

    def DoManifest(NAME:str, CLASS:type, REQUIRES:list[str|tuple[str,str]], Description:str|List[str]="") -> str:
        """generates manifests quickly for use here"""
        from manifest import ManifestGenerator
        import json
        manifest = ManifestGenerator(NAME,CLASS,REQUIRES,__file__,["NadirRift"],Description)
        manifest.DateGenearted = ""
        manifest.Hash = "BACKSLSH:"
        output = "@MANIFEST\n"+json.dumps({k: v for k, v in manifest.__dict__.items() if not k.startswith("_")},indent=2)
        print(output)
        return output

    import autoit

    class AutoITMouse(MouseBase):
        """
        @MANIFEST
        {
            "Name": "Mouse_AutoIt",
            "Class": "AutoITMouse",
            "BaseClass": "MouseBase",
            "Requirements": [["autoit","0.2.6"]],
            "FILE": "kbm_base.py",
            "Hash": "BACKSLSH:",
            "Author": ["NadirRift"],
            "Description": ["Mouse AutoIt Abstraction layer for Macroing"],
            "DateGenearted": ""
        }        ^BLANK ON PURPOSE BUT WOULD LOOK LIKE
            "DateGenearted":"28/12/2030 12:00 GMT+0000"
        """
        @staticmethod
        def mouse_click(button = Mouse.LEFT, x = INTDEFAULT, y = INTDEFAULT, clicks = CLICK_DEFAULT, speed = SPEED_DEFAULT):
            return autoit.mouse_click(button,x,y,clicks,speed)

        @staticmethod
        def mouse_click_drag(x1, y1, x2, y2, button = Mouse.LEFT, speed = SPEED_DEFAULT):
            return autoit.mouse_click_drag(x1,y1,x2,y2,button,speed)

        @staticmethod
        def mouse_down(button = Mouse.LEFT):
            return autoit.mouse_down(button)

        @staticmethod
        def mouse_up(button = Mouse.LEFT):
            return autoit.mouse_up(button)
        
        @staticmethod
        def mouse_get_pos():
            return autoit.mouse_get_pos() # TEST

        @staticmethod
        def mouse_move(x, y, speed = SPEED_DEFAULT):
            return autoit.mouse_move(x,y,speed)
        
        @staticmethod
        def mouse_wheel(direction, clicks = CLICK_DEFAULT):
            return autoit.mouse_wheel(direction,clicks)

    import keyboard

    class AutoITKeyboard(KeyboardBase):
        """
        @MANIFEST
        {
            "Name": "Keyboard_and_AutoIt",
            "Class": "AutoITKeyboard",
            "BaseClass": "KeyboardBase",
            "Requirements": [
                ["keyboard","0.13.5"],
                ["autoit","0.2.6"]
            ],
            "FILE": "kbm_base.py",
            "Hash": "BACKSLSH:",
            "Author": ["NadirRift"],
            "Description": ["Keyboard and AutoIt Abstraction layer for Macroing"],
            "DateGenearted": ""
        }
        """
        @staticmethod
        def setClipboard(text):
            return autoit.clip_put(text)

        @staticmethod
        def getClipboard():
            return autoit.clip_get()

        @staticmethod
        def press(key):
            return keyboard.press(key)

        @staticmethod
        def release(key):
            return keyboard.release(key)

        @staticmethod
        def is_pressed(key):
            return keyboard.is_pressed(key)

        @staticmethod
        def key_to_scan_codes(key, error_if_missing=True):
            return keyboard.key_to_scan_codes(key,error_if_missing)

        @staticmethod
        def is_modifier(key):
            return keyboard.is_modifier(key)

        @staticmethod
        def send(send_text, mode=0):
            return autoit.send(send_text,mode)
        
    class StandaloneKeyboard(KeyboardBase):
        """
        @MANIFEST
        {

            "Name": "Keyboard",
            "Class": "StandaloneKeyboard",
            "BaseClass": "KeyboardBase",
            "Requirements": [["keyboard","0.13.5"]],
            "FILE": "kbm_base.py",
            "Hash": "BACKSLSH:",
            "Author": ["NadirRift"],
            "Description": [
                "Standard Keyboard Abstraction layer for Macroing",
                "Its pretty awefully implemented... oops :P"
            ],
            "DateGenearted": ""
        }
        """
        __CLIPBOARD_FAKE:str
        CACHE:dict[str,list[function]]=[]

        @staticmethod
        def setClipboard(text):
            """
            no standard way to set clipboard with keyboard module
            that i know of so we emulate it here
            """
            StandaloneKeyboard.__CLIPBOARD_FAKE = text
            return text

        @staticmethod
        def getClipboard():
            return StandaloneKeyboard.__CLIPBOARD_FAKE

        @staticmethod
        def press(key):
            return keyboard.press(key)

        @staticmethod
        def release(key):
            return keyboard.release(key)

        @staticmethod
        def is_pressed(key):
            return keyboard.is_pressed(key)

        @staticmethod
        def key_to_scan_codes(key, error_if_missing=True):
            return keyboard.key_to_scan_codes(key,error_if_missing)

        @staticmethod
        def is_modifier(key):
            return keyboard.is_modifier(key)
        
        @staticmethod
        def send(send_text:str, mode:int|bool=0):
            #if mode 1 we just send the stuff over unchanged
            if int(mode) == 1:
                #easy in, easy out
                keyboard.write(send_text,exact=True)
            else:
                #retrieve current mode by default it's using the autoit syntax
                MODE = KeyboardBase.CURRENT_MODE
                cache_key_str = StandaloneKeyboard.fnv_hash_64a(send_text)
                message_hash  = f"{MODE}:{cache_key_str}"

                #quick hash the text so that if we have already run this string
                #before we don't need to recompute the output
                if message_hash in StandaloneKeyboard.CACHE:
                    cached_result = StandaloneKeyboard.CACHE[message_hash]
                else:
                    #oh fun, we have no cache for this text
                    #time to build one
                    MAPPING = KeyboardBase.CURRENT
                    #sort mapping keys from biggest to smallest, making it easier to retrieve keys
                    sort = sorted(MAPPING.keys(),key=len,reverse=True)
                    #initialise variables so we don't throw errors
                    #may have forgotten to do this once or twice
                    cached_result:list[function] = []
                    char_index = 0
                    message=""
                    send_text_length = len(send_text)
                    #loop over mess|age using an index
                    #essantially a ^ cursor
                    #           like that
                    while char_index < send_text_length:
                        matched = False
                        #loop of keys in our big_lil sorted list
                        for key in sort:
                            #if our text STARTS WITH the key we do some evil magic
                            if send_text.startswith(key, char_index):
                                val = MAPPING[key]
                                #if our mapping is greater then 1 then we have
                                #a specific output needed for this mode
                                if len(val) > 1:
                                    #we grab the key
                                    special_key = val[1]
                                    #only if its message is greater then 0
                                    #cause we don't want to send an empty
                                    if len(message) > 0:
                                        #and shove it and our precache
                                        cached_result.append(lambda text=message, key=special_key:(keyboard.write(text,exact=True),keyboard.send(key)))
                                    else:
                                        cached_result.append(lambda key=special_key:(keyboard.send(key)))
                                    #ALWAYS RESET THE MESSAGE, even if its already blank
                                    #its just good practice
                                    message = ""
                                else:
                                    #dump the last key to the precache
                                    cached_result.append(lambda k=special_key: keyboard.send(k))
                                #increment by size of the key we just index
                                char_index += len(key)
                                #send a match
                                matched = True
                                #break the for loop
                                break
                        #if no match we just add the last character to the message block
                        if not matched:
                            message += send_text[char_index]
                            #incrementing the index
                            char_index += 1
                    #flush out the message if anything is left!
                    if message:
                        cached_result.append(lambda s=message: keyboard.write(s, exact=True))
                    #SAVE THAT CACHE UNDER OUR HASH!
                    StandaloneKeyboard.CACHE[message_hash] = cached_result
                #finally after the IF/ELSE
                #we loop over the cached lambda calls
                #doing a listed keyboard outputs :D
                for func in cached_result:
                    func()
            #return None because thats what "keyboard" does
            return None

        def fnv_hash_64a(string:str) :
            """
            please go see: https://github.com/lcn2/fnv/blob/master/hash_64a.c \n
            just a yoink so we can have a storage method that doesn't use sha256
            for hashing
            """
            hash_num = 0xCBF29CE484222325
            fnv1_prime = 0x100000001B3
            mask = 0xFFFFFFFFFFFFFFFF
            for byte in string.encode("utf-8"):
                hash_num = ((hash_num ^ byte) * fnv1_prime) & mask
            return hash_num





    if False:
        
        #TODO: Handle with @Manifest File Handler
        MouseBase.__INSTANCES = {}
        MouseBase.__INSTANCES["Mouse_AutoIt"] = AutoITMouse()

        KeyboardBase.__INSTANCES = {}
        KeyboardBase.__INSTANCES["Keyboard_and_AutoIt"]   = AutoITKeyboard()
        KeyboardBase.__INSTANCES["keyboard"] = StandaloneKeyboard()
            
        DoManifest(
            "Mouse_AutoIt",
            AutoITMouse,
            [("autoit","0.2.6")],
            Description=["Mouse AutoIt Abstraction layer for Macroing"])
        
        DoManifest(
            "Keyboard_and_AutoIt",
            AutoITKeyboard,
            [("keyboard","0.13.5"),("autoit","0.2.6")],
            Description=["Keyboard and AutoIt Abstraction layer for Macroing"])

        #standalone keyboard module
        DoManifest(
            "Keyboard",
            StandaloneKeyboard,
            [("keyboard","0.13.5")],
            Description=["Standard Keyboard Abstraction layer for Macroing","Its pretty awefully implemented... oops :P"])
finally:pass