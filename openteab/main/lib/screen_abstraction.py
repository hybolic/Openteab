from __future__ import annotations
from enum import IntFlag
from struct import unpack
from typing import Any, get_args, Literal, Final
from abc import ABC, abstractmethod
import platform as _platform

try: from openteab.main.lib.Exceptions import DuplicateRegistryError, GetTypeName; from openteab.main.lib.decorators import classproperty
except ImportError:    from Exceptions import DuplicateRegistryError, GetTypeName;                   from decorators import classproperty


try: from openteab.main.lib.decorators import single
except ImportError: from decorators import single

TEST = False

#over engineered asf flags
class PixelMode(IntFlag):
    #slow takes priority
    SLOW     =0b100000000 #use force slow when availble
    #then alt
    ALT      =0b000000001 #use alt mode
    #Default
    NONE     =0b000000000 #no attribute flags
    
    # flag components
    #     you can use this but best you stick with the pre-defined ones

    #include alpha
    ALPHA        =0b000000010 #include alpha

    #flips for BGR(A?)
    IN_BGR_FLIP  =0b000010000 #bgr color in flip flag
    OUT_BGR_FLIP =0b010000000 #bgr color out flip flag

    #search flag RGB (byte)(byte)(byte)(byte?) or (int)(int)(int)(int?)
    RGB          =0b000000100 
    BGR      =IN_BGR_FLIP | RGB

    #search flag HEX (FF)(FF)(FF)(FF?)
    HEX          =0b000001000
    BGRHEX   = IN_BGR_FLIP | HEX

    #OUT FLAGS
    OUT_RGB      =0b000100000 #out RGB
    OUT_BGR  = OUT_BGR_FLIP | OUT_RGB
    
    OUT_HEX      =0b001000000 #out HEX
    OUT_BGRHEX= OUT_BGR_FLIP | OUT_BGR

    #USE THESE FLAGS
    RGB_IN_RGB_OUT = RGB | OUT_RGB
    BGR_IN_BGR_OUT = BGR | OUT_BGR
    RGB_IN_BGR_OUT = RGB | OUT_BGR
    BGR_IN_RGB_OUT = BGR | OUT_RGB
    
    HEX_IN_HEX_OUT       =    HEX | OUT_HEX
    HEX_IN_BGRHEX_OUT    =    HEX | OUT_BGRHEX
    BGRHEX_IN_HEX_OUT    = BGRHEX | OUT_HEX
    BGRHEX_IN_BGRHEX_OUT = BGRHEX | OUT_BGRHEX

    RGB_IN_BGRHEX_OUT =    RGB | OUT_BGRHEX
    RGB_IN_HEX_OUT    =    RGB | OUT_HEX
    BGR_IN_BGRHEX_OUT =    BGR | OUT_BGRHEX
    BGR_IN_HEX_OUT    =    BGR | OUT_HEX
    HEX_IN_RGB_OUT    =    HEX | OUT_RGB
    HEX_IN_BGR_OUT    =    HEX | OUT_BGR
    BGRHEX_IN_RGB_OUT = BGRHEX | OUT_RGB
    BGRHEX_IN_BGR_OUR = BGRHEX | OUT_BGR

    ALPHA_RGB_IN_RGB_OUT       = ALPHA |    RGB | OUT_RGB
    ALPHA_BGR_IN_BGR_OUT       = ALPHA |    BGR | OUT_BGR
    ALPHA_RGB_IN_BGR_OUT       = ALPHA |    RGB | OUT_BGR
    ALPHA_BGR_IN_RGB_OUT       = ALPHA |    BGR | OUT_RGB
    ALPHA_HEX_IN_HEX_OUT       = ALPHA |    HEX | OUT_HEX
    ALPHA_HEX_IN_BGRHEX_OUT    = ALPHA |    HEX | OUT_BGRHEX
    ALPHA_BGRHEX_IN_HEX_OUT    = ALPHA | BGRHEX | OUT_HEX
    ALPHA_BGRHEX_IN_BGRHEX_OUT = ALPHA | BGRHEX | OUT_BGRHEX
    ALPHA_RGB_IN_BGRHEX_OUT    = ALPHA |    RGB | OUT_BGRHEX
    ALPHA_RGB_IN_HEX_OUT       = ALPHA |    RGB | OUT_HEX
    ALPHA_BGR_IN_BGRHEX_OUT    = ALPHA |    BGR | OUT_BGRHEX
    ALPHA_BGR_IN_HEX_OUT       = ALPHA |    BGR | OUT_HEX
    ALPHA_HEX_IN_RGB_OUT       = ALPHA |    HEX | OUT_RGB
    ALPHA_HEX_IN_BGR_OUT       = ALPHA |    HEX | OUT_BGR
    ALPHA_BGRHEX_IN_RGB_OUT    = ALPHA | BGRHEX | OUT_RGB
    ALPHA_BGRHEX_IN_BGR_OUT    = ALPHA | BGRHEX | OUT_BGR

    @classmethod
    def removeFlag(cls,FLAGS,FLAG:PixelMode)  -> int|PixelMode:
        return FLAG.remove(FLAGS)
    
    def remove(self,FLAGS) -> int|PixelMode:
        result = FLAGS & ~self
        try:
            return PixelMode(result)
        except ValueError:
            return result

    @classmethod
    def hasFlag(cls,FLAGS,MODE:PixelMode) -> bool:
        return MODE.isIn(FLAGS)
    
    def isIn(self,FLAG) -> bool:
        if self == PixelMode.NONE:
            return FLAG == 0
        return self & FLAG == self
    @staticmethod
    def TryGet(FLAGS:int):
        try:
            return PixelMode(FLAGS)
        except ValueError:
            return FLAGS
    @classmethod
    def getFlagsClass(cls,FLAGS) -> list[PixelMode]:
        LIST:list[PixelMode] = []
        for Flag in PixelMode:            #is compound
            if Flag == PixelMode.NONE or (Flag & (Flag - 1)):
                continue
            elif Flag.isIn(FLAGS):
                LIST.append(Flag)
        if len(LIST) == 0:
            LIST.append(PixelMode.NONE)
        return LIST

    __MAX = ((SLOW << 1) -1)
    @staticmethod
    def limitLength(FLAGS):
        output = FLAGS & PixelMode.__MAX
        try:
            return PixelMode(output)
        except ValueError:
            return output

removeAlt = PixelMode.ALT.removeFlag
hasSlow = PixelMode.SLOW.isIn
limitMode = PixelMode.limitLength

def preProcessMode(Mode):
    Mode = limitMode(Mode)
    if hasSlow(Mode):
        Mode = removeAlt(Mode)
    return Mode

class ScreenBase(ABC):
    
    @classproperty
    def CURRENT_INSTANCE() -> ScreenBase:
        return next(iter(ScreenBase.__INSTANCES.values()), None)
    
    __INSTANCES:dict[ScreenBase] = dict()
    __INSTANCES_TYPES:set[type]  = set()

    @staticmethod
    def Register(KEY:str, cls:ScreenBase):
        if KEY in ScreenBase.__INSTANCES:
            raise DuplicateRegistryError(f"{GetTypeName(cls)}: The Key, '{KEY}' has already been registered.")
        else:
            if type(cls) in ScreenBase.__INSTANCES_TYPES:
                print(f"The Class '{GetTypeName(cls)}'({KEY}) has already been registered. This could be a mistake!")
        
        #add to lookup for class check
        ScreenBase.__INSTANCES_TYPES.add(type(cls))

        #registry
        ScreenBase.__INSTANCES.update({KEY:cls})

    def register(self, KEY:str, cls:ScreenBase=None):
        if cls == None:
            ScreenBase.Register(KEY,self)
        else:
            ScreenBase.Register(KEY,cls)
        
    
    def __init__(self,KEY:str):
        super().__init__()
        self.register(KEY)

    @classmethod
    def PixelGetColor(cls,x:int,y:int,Mode:PixelMode|int=PixelMode.RGB):
        return ScreenBase.CURRENT_INSTANCE._pixelGetColor(x,y,Mode)
    
    @classmethod
    def PixelCheckColor(cls,x:int,y:int,Color:int|str|tuple[int,int,int,int|None],Variation:int|str|tuple[int,int,int,int|None],Mode:PixelMode|int=PixelMode.RGB_IN_RGB_OUT) -> bool:
        try:
            return ScreenBase.CURRENT_INSTANCE._pixelCheckColor(x,y,Color,Variation,Mode)
        except NotImplementedError:
            USE_ALPHA = PixelMode.hasFlag(Mode, PixelMode.ALPHA)
            if isinstance(Variation, tuple):
                T_R = Variation[0]
                T_G = Variation[1] if len(Variation) > 1 else Variation[0]
                T_B = Variation[2] if len(Variation) > 2 else Variation[0]
                if USE_ALPHA:
                    T_A = Variation[3] if len(Variation) > 3 and Variation[3] is not None else Variation[0]
            elif isinstance(Variation, (str,int)):
                if isinstance(Variation,str):
                    Variation = int(Variation, 16)
                T_R =  Variation        & 0xff
                T_G = (Variation >>  8) & 0xff
                T_B = (Variation >> 16) & 0xff
                if USE_ALPHA:
                    T_A = (Variation >> 24) & 0xff
            else:
                raise TypeError(f"Type {GetTypeName(Variation)} for Variation, is invalid!")

            if isinstance(Color, tuple):
                R = Color[0]
                G = Color[1] if len(Color) > 1 else Color[0]
                B = Color[2] if len(Color) > 2 else Color[0]
                if USE_ALPHA:
                    A = Color[3] if len(Color) > 3 and Color[3] is not None else 255
            elif isinstance(Color, (str,int)):
                if isinstance(Color,str):
                    Color = int(Color, 16)
                R =  Color        & 0xff
                G = (Color >>  8) & 0xff
                B = (Color >> 16) & 0xff
                if USE_ALPHA:
                    A = (Color >> 24) & 0xff
            else:
                raise TypeError(f"Type {GetTypeName(Color)} for Color, is invalid!")
            
            if PixelMode.hasFlag(Mode, PixelMode.IN_BGR_FLIP):
                B,R    = R,B
                T_B,T_R = T_R,T_B

            R_MIN = max(  0, R - T_R);R_MAX = min(255, R + T_R)
            G_MIN = max(  0, G - T_G);G_MAX = min(255, G + T_G)
            B_MIN = max(  0, B - T_B);B_MAX = min(255, B + T_B)
            if USE_ALPHA:
                A_MIN = max(  0, A - T_A);A_MAX = min(255, A + T_A)

            ALPHA      = PixelMode.ALPHA if USE_ALPHA else PixelMode.NONE
            COLOR_MODE = PixelMode.BGR if PixelMode.hasFlag(Mode, PixelMode.OUT_BGR_FLIP) else PixelMode.RGB
            PIXEL_MODE = PixelMode.TryGet(ALPHA | COLOR_MODE | PixelMode.OUT_RGB)
            
            #Fast Row Search
            buffer = ScreenBase.CURRENT_INSTANCE._pixelGetColor(x,y,PIXEL_MODE)
            
            r = buffer[0]
            g = buffer[1]
            b = buffer[2]

            if USE_ALPHA:
                a = buffer[3]
                return (R_MIN <= r <= R_MAX) and (G_MIN <= g <= G_MAX) and (B_MIN <= b <= B_MAX) and (A_MIN <= a <= A_MAX)
            else:
                return (R_MIN <= r <= R_MAX) and (G_MIN <= g <= G_MAX) and (B_MIN <= b <= B_MAX)

    @abstractmethod
    def _pixelCheckColor(self,x:int,y:int,Color:int|str|tuple[int,int,int,int|None],Variation:int|str|tuple[int,int,int,int|None],Mode:PixelMode|int=PixelMode.RGB) -> bool:
        #NOTE: Does NOT need to be implemented! The fallback is fast enough
        raise NotImplementedError
    
    @abstractmethod
    def _pixelGetColor(self,x:int,y:int,Mode:PixelMode|int=PixelMode.NONE):
        raise NotImplementedError

    @classmethod
    def PixelSearch(cls,x1:int,y1:int,x2:int,y2:int,Color:int|str|tuple[int,int,int,int|None],Variation:int|str|tuple[int,int,int,int|None],Mode:PixelMode|int=PixelMode.RGB,WidthHeight=False):
        return ScreenBase.CURRENT_INSTANCE._pixelSearch(x1,y1,x2,y2,Color,Variation,Mode,WidthHeight)

    @abstractmethod
    def _pixelSearch(self,x1:int,y1:int,x2:int,y2:int,Color:int|str|tuple[int,int,int,int|None],Variation:int|str|tuple[int,int,int,int|None],Mode:PixelMode|int=PixelMode.RGB,WidthHeight=False):
        raise NotImplementedError
            
    @classmethod
    def ImageSearch(cls,x1:int,y1:int,x2:int,y2:int,ImageFile:str|Any,Variation,Mode):
        return ScreenBase.CURRENT_INSTANCE._imageSearch(x1,y1,x2,y2,ImageFile,Variation,Mode)

    @classmethod
    @abstractmethod
    def _imageSearch(self,x1:int,y1:int,x2:int,y2:int,ImageFile:str|Any,Variation,Mode):
        raise NotImplementedError

try:
    from mss.base import MSSBase, ScreenShot
    
    @single
    class MSS_Screen(ScreenBase):
        __sct:MSSBase

        def __init__(self, KEY):
            super().__init__(KEY)
            from mss import mss
            self.__sct = mss()
            try:
                from numpy import frombuffer, argwhere, uint8
                self.__fromBuffer = lambda value: frombuffer(value,uint8)
                self.__argwhere   = lambda mask : argwhere(mask)
            except ImportError: self.__fromBuffer = None
            

        def GrabFromPoints(self,x1:int|float,y1:int|float,x2:int|float,y2:int|float,HANDLE_ERROR=False) -> ScreenShot:
            x      = int(min(x1,x2))
            y      = int(min(y1,y2))
            width  = int(abs(x2 - x1))
            height = int(abs(y2 - y1))
            if width <= 0:
                if HANDLE_ERROR: width = 1
                else: raise ValueError("Selection Width must be greater then 0")
            if height <= 0:
                if HANDLE_ERROR: height = 1
                else: raise ValueError("Selection Height must be greater then 0")
            return self.GrabRect(x,y,width,height,HANDLE_ERROR)
        
        def GrabRect(self, x:int|float, y:int|float, width:int|float=int(1), height:int|float=int(1),HANDLE_ERROR=False) -> ScreenShot:
            if width <= 0:
                if HANDLE_ERROR: width = 1
                else: raise ValueError("Selection Width must be greater then 0")
            if height <= 0:
                if HANDLE_ERROR: height = 1
                else: raise ValueError("Selection Height must be greater then 0")
            return self.__sct.grab({"left": int(x), "top": int(y), "width": int(width), "height": int(height)})

        def _pixelGetColor(self, x, y, Mode = PixelMode.RGB):
            shot = self.GrabRect(x,y)
            return self._pixelGetColorFromShot(shot,0,0,Mode)
        
        def _pixelGetColorFromShot(self, shot:ScreenShot, x, y, Mode = PixelMode.RGB):
            if len(shot.bgra) > 4:
                offset = (shot.width * y + x) * 4
                B,G,R,A = shot.bgra[offset : offset + 4]
            else:
                B,G,R,A = (int(c) for c in shot.bgra[:4]) # Ensure Integer before processing
            if(PixelMode.hasFlag(Mode, PixelMode.OUT_BGR_FLIP)):
                R, B = B, R
            if(PixelMode.hasFlag(Mode, PixelMode.OUT_HEX)):
                B,G,R,A = (f"{c:02X}" for c in (B,G,R,A))
            if PixelMode.hasFlag(Mode, PixelMode.ALPHA):
                return R,G,B,A
            return R,G,B
        
        PIXEL_ALPHA = (PixelMode.BGR_IN_RGB_OUT | PixelMode.ALPHA)
        def _pixelSearch(self, x1, y1, x2, y2, Color:int|str|tuple[int,int,int,int|None], Variation:int|str|tuple[int,int,int,int|None], Mode = PixelMode.RGB,WidthHeight=False) -> tuple[int,int]:
            if WidthHeight:
                shot = self.GrabRect(x1,y1,x2,y2)
                w, h = x2, y2
            else:
                shot = self.GrabFromPoints(x1,y1,x2,y2)
                w, h = max(abs(x2-x1),1), max(abs(y1-y2),1)

            USE_ALPHA = PixelMode.hasFlag(Mode, PixelMode.ALPHA)

            if isinstance(Variation, tuple):
                T_R = Variation[0]
                T_G = Variation[1] if len(Variation) > 1 else Variation[0]
                T_B = Variation[2] if len(Variation) > 2 else Variation[0]
                if USE_ALPHA:
                    T_A = Variation[3] if len(Variation) > 3 and Variation[3] is not None else Variation[0]
            elif isinstance(Variation, (str,int)):
                if isinstance(Variation,str):
                    Variation = int(Variation, 16)
                T_R =  Variation        & 0xff
                T_G = (Variation >>  8) & 0xff
                T_B = (Variation >> 16) & 0xff
                if USE_ALPHA:
                    T_A = (Variation >> 24) & 0xff
            else:
                raise TypeError(f"Type {GetTypeName(Variation)} for Variation, is invalid!")

            if isinstance(Color, tuple):
                R = Color[0]
                G = Color[1] if len(Color) > 1 else Color[0]
                B = Color[2] if len(Color) > 2 else Color[0]
                if USE_ALPHA:
                    A = Color[3] if len(Color) > 3 and Color[3] is not None else 255
            elif isinstance(Color, (str,int)):
                if isinstance(Color,str):
                    Color = int(Color, 16)
                R =  Color        & 0xff
                G = (Color >>  8) & 0xff
                B = (Color >> 16) & 0xff
                if USE_ALPHA:
                    A = (Color >> 24) & 0xff
            else:
                raise TypeError(f"Type {GetTypeName(Color)} for Color, is invalid!")
            
            if PixelMode.hasFlag(Mode, PixelMode.IN_BGR_FLIP):
                B,R    = R,B
                T_B,T_R = T_R,T_B

            R_MIN = max(  0, R - T_R)
            R_MAX = min(255, R + T_R)
            G_MIN = max(  0, G - T_G)
            G_MAX = min(255, G + T_G)
            B_MIN = max(  0, B - T_B)
            B_MAX = min(255, B + T_B)
            if USE_ALPHA:
                A_MIN = max(  0, A - T_A)
                A_MAX = min(255, A + T_A)

            #fast when Numpy is Availble
            if self.__fromBuffer is not None and not PixelMode.hasFlag(Mode, PixelMode.SLOW):
                img = self.__fromBuffer(shot.bgra).reshape(h,w,4)
                b,g,r,a = img[:, :, 0], img[:, :, 1], img[:, :, 2], img[:, :, 3]
                
                if USE_ALPHA:
                    mask = ((b >= B_MIN) & (b <= B_MAX)
                        &(g >= G_MIN) & (g <= G_MAX)
                        &(r >= R_MIN) & (r <= R_MAX)
                        &(a >= A_MIN) & (a <= A_MAX))
                else:
                    mask = ((b >= B_MIN) & (b <= B_MAX)
                        &(g >= G_MIN) & (g <= G_MAX)
                        &(r >= R_MIN) & (r <= R_MAX))
                    
                matches = self.__argwhere(mask)
                
                if matches.size > 0:
                    y, x = matches[0]
                    return int(x+x1),int(y+y1)
                return None
            
            #Slow Column Search
            if PixelMode.hasFlag(Mode, PixelMode.SLOW):
                for x in range(w):
                    for y in range(h):
                        ind = (y*shot.width + x) * 4
                        abs_x = x1 + x
                        abs_y = y1 + y
                        r,g,b,a = shot.bgra[ind:ind+4] #force RGBA output
                        if (R_MIN <= r <= R_MAX) and (G_MIN <= g <= G_MAX) and (B_MIN <= b <= B_MAX) and (A_MIN <= a <= A_MAX if USE_ALPHA else True):
                            return abs_x,abs_y
                return None
            
            #Fast Row Search
            buffer = shot.bgra
            row_bytes = w << 2
            if USE_ALPHA:
                for y in range(h):
                    ind = y * row_bytes
                    for x in range(w):
                        b = buffer[ind]
                        g = buffer[ind+1]
                        r = buffer[ind+2]
                        a = buffer[ind+3]
                        if (R_MIN <= r <= R_MAX) and (G_MIN <= g <= G_MAX) and (B_MIN <= b <= B_MAX) and (A_MIN <= a <= A_MAX):
                            return x+x1,y+y1
                        ind += 4
            else:
                for y in range(h):
                    ind = y * row_bytes
                    for x in range(w):
                        b = buffer[ind]
                        g = buffer[ind+1]
                        r = buffer[ind+2]
                        if (R_MIN <= r <= R_MAX) and (G_MIN <= g <= G_MAX) and (B_MIN <= b <= B_MAX):
                            return x+x1,y+y1
                        ind += 4
            return None

        def _imageSearch(self, x1, y1, x2, y2, ImageFile, Variation, Mode):
            raise NotImplementedError("Currently Not implmented for Pure MSS")

        def _pixelCheckColor(self, x, y, Color, Variation, Mode = PixelMode.NONE):
            raise NotImplementedError
    MSS_Screen("MSS_Screen")

    if TEST:
        print("START TESTS")
        print(ScreenBase.PixelGetColor(0,0))
        print(ScreenBase.PixelGetColor(0,0,PixelMode.OUT_BGR|PixelMode.ALPHA))
        print(ScreenBase.PixelCheckColor(0,0,(25, 26, 27),PixelMode.RGB_IN_RGB_OUT))
        print(ScreenBase.PixelSearch(0,0,1280,720,(255,255,255),(10,10,10),PixelMode.RGB_IN_RGB_OUT,True))
        print(ScreenBase.PixelSearch(0,0,1280,720,(255,255,255),(0,0,0),PixelMode.RGB_IN_RGB_OUT,True))
        print(ScreenBase.PixelSearch(0,0,50,50,(25, 26, 27),(0,0,0),PixelMode.RGB_IN_RGB_OUT,True))
    
except ImportError:
    print("WHY DO WE NOT HAVE Multi SCREENSHOT!?")
    pass
