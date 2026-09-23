from __future__ import annotations

import asyncio
from asyncio import CancelledError, TimeoutError
import time
from main import Api
import inspect
from typing import Any, Callable, Coroutine, overload
from abc import ABC, abstractmethod

from typing import Any, Callable

try:
    from openteab.main.mixin.mixin_actions import ActionsMixin
except:
    class ActionsMixin():pass

try:
    from openteab.globals import roblox
except:
    roblox = []

class MACRO_BASE(ABC):

    def __init__(self, owner:Api, tracker:ActionsMixin, PRE_LOOP_REQUIRED:bool=False, POST_LOOP_REQUIRED:bool=False, PRE_LOOP_ENABLED:bool=False, POST_LOOP_ENABLED:bool=False):

        self.PRE_LOOP_ENABLED  = PRE_LOOP_ENABLED or PRE_LOOP_REQUIRED
        self.POST_LOOP_ENABLED = POST_LOOP_ENABLED or POST_LOOP_REQUIRED

        self.PRE_LOOP_REQUIRED  = PRE_LOOP_REQUIRED
        self.POST_LOOP_REQUIRED = POST_LOOP_REQUIRED
        
        self.LOOP_MAIN : asyncio.Task | None = None
        self.PRE_TASK  : asyncio.Task | None = None
        self.LOOP_TASK : asyncio.Task | None = None
        self.POST_TASK : asyncio.Task | None = None

        #techically shouldn't be directly accessed
        self.__running = False
        self.__busy    = False

        #the only callbacks that should be registered
        self._hotkey_start_callbacks: list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []
        self._hotkey_stop_callbacks:  list[tuple[Callable[..., Any], tuple[Any, ...], dict[str, Any]]] = []

        self._owner:Api = owner
        self._tracker:ActionsMixin = tracker

        #used in print to get the name of the class being used
        self.__classname__ = self.__class__.__name__
        self.__RESTRICT_CALLBACK_DUPLICATES = False
        self.__configProvider:Callable[[], dict[str, Any]] | None = None

    '''restrict duplicates in callbacks'''
    @property
    def RESTRICT_CALLBACK_DUPLICATES(self) -> bool: return self.__RESTRICT_CALLBACK_DUPLICATES
    @RESTRICT_CALLBACK_DUPLICATES.setter
    def RESTRICT_CALLBACK_DUPLICATES(self,RESTRICT_CALLBACK_DUPLICATES:bool):self.__RESTRICT_CALLBACK_DUPLICATES = bool(RESTRICT_CALLBACK_DUPLICATES)



    '''busy property'''
    @property
    def busy(self) -> bool: return self.__busy
    @busy.setter
    def busy(self,BUSY:bool):self.__busy = bool(BUSY)

    '''non-property functions'''
    def isBusy(self)->bool: return self.busy
    def setBusy(self,BUSY:bool=True): self.busy = BUSY; return self
    def setNotBusy(self):return self.setBusy(False)

    '''config provider'''
    def configProvider(self) -> Callable[[], dict[str, Any]] | None: return self.__configProvider
    def setConfigProvider(self, provider:Callable[[], dict[str, Any]]): self.__configProvider = provider; return self
    
    '''running property'''
    @property
    def running(self) -> bool: return self.__running
    @running.setter
    def running(self,RUNNING:bool):self.__running = bool(RUNNING)

    '''non-property functions'''
    def isRunning(self)->bool: return self.running
    def setRunning(self,RUNNING:bool=True): self.running = RUNNING; return self
    def setNotRunning(self):return self.setRunning(False)



    def getOwner(self):return self._owner
    def getTracker(self):return self._tracker

    def getClassName(self) -> str:
        try:
            return self.__classname__
        except AttributeError:
            self.__classname__ = type(self).__name__
            return self.__classname__
        
    #NOTE
    '''TEST AND EXAMPLE ON HOW TO CALL LOOP'''
    async def call_loop_test(self):
        self.LOOP_MAIN  = asyncio.create_task(self.LOOP())
        TEMP = self
        def temp():
            if TEMP.isRunning():
                print("LOOP IS DONE!")
            else:
                print("LOOP DIDN'T FINISH!")
        self.LOOP_MAIN.add_done_callback(lambda _:temp())
        return self.LOOP_MAIN
        
    @staticmethod
    @overload
    async def DO_TASK_SAFELY(the_func:Coroutine, is_required:bool,timeout:float|bool|None=None) -> asyncio.Task: ...
    
    @staticmethod
    @overload
    async def DO_TASK_SAFELY(the_func:Callable, is_required:bool,timeout:float|bool|None=None, *args, **kwargs) -> asyncio.Task: ...

    @staticmethod
    async def DO_TASK_SAFELY(the_func:Coroutine|Callable, is_required:bool, timeout:float|bool|None=None, args: tuple[Any, ...] = (), kwargs: dict[str, Any] | None = None) -> asyncio.Task:
        if kwargs is None: kwargs = {}
        # the thought behind timeout being float and bool was that if its passed a True, then yes it has a timeout but a function that normally would run very quick 
        # and this is just there to catch it if it hangs to long, but timeout as float with the minimum of 30 seconds was more
        # application should take x time to complete where 30 seconds is the bare minimum
        if timeout is not None:
            if isinstance(timeout, bool):
                if timeout: timeout = 5.0 #does fast, used only for debugging and shouldn't be used normally
                else: timeout = None
            else: timeout = max(float(timeout),30.0) #30 second minimium
        
        if inspect.iscoroutine(the_func):
            task = asyncio.create_task(the_func)
        elif inspect.iscoroutinefunction(the_func):
            task = asyncio.create_task(the_func(*args, **kwargs))
        else:
            task = asyncio.create_task(asyncio.to_thread(the_func, *args, **kwargs)) # the function we are doing safely wrapped in an asyncio task

        if is_required:
            try:
                if timeout is None:
                    while not task.done():
                        try:
                            await asyncio.shield(task)
                        except CancelledError: continue #ignore attempts to cancel the process
                else:
                    async with asyncio.timeout(timeout):
                        while not task.done():
                            try: await asyncio.shield(task)
                            except CancelledError: continue #ignore attempts to cancel the process
            except TimeoutError:
                task.cancel()
                await asyncio.gather(task,return_exceptions=True)
                raise #if timed-out kill task and send exceptions caused by that up the chain

        else:
            try:
                if timeout is None: await task
                else:
                    async with asyncio.timeout(timeout): await task
            except CancelledError:
                if not task.done():
                    task.cancel()
                    await asyncio.gather(task, return_exceptions=True)
                raise #kill task and send exceptions caused by that up the chain
            except TimeoutError:
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
                raise #if timed out kill task and send exceptions caused by that up the chain
        return task
    
    async def LOOP(self, *args, **kwargs):
        if self.isRunning():
            return
        self.setRunning()

        try:
            if self.PRE_LOOP_ENABLED:
                self.PRE_TASK = await MACRO_BASE.DO_TASK_SAFELY(self.pre_loop, self.PRE_LOOP_REQUIRED, None, args, kwargs)
            self.PRE_TASK = None
            if self.isRunning():
                self.LOOP_TASK = asyncio.create_task(self.loop(*args, **kwargs))
        finally:
            try:
                if self.isRunning():
                    await self.LOOP_TASK
            finally:
                self.LOOP_TASK = None
                try:
                    if self.POST_LOOP_ENABLED and self.isRunning():
                        self.POST_TASK = await MACRO_BASE.DO_TASK_SAFELY(self.post_loop, self.POST_LOOP_REQUIRED, None, args, kwargs)
                finally: self.POST_TASK = None
        self.setNotRunning()

    async def CANCEL(self):
        if self.isRunning():
            self.setNotRunning() #force it off
            #check all loops anc cancel them
            if self.PRE_TASK and not self.PRE_TASK.done() and not self.PRE_LOOP_REQUIRED:
                self.PRE_TASK.cancel()
            if self.LOOP_TASK and not self.LOOP_TASK.done():
                self.LOOP_TASK.cancel()
            if self.POST_TASK and not self.POST_TASK.done() and not self.POST_LOOP_REQUIRED:
                self.POST_TASK.cancel()
            await asyncio.gather(self.LOOP_MAIN, return_exceptions=True)
            print("MACRO LOOP CANCELLED")

    def _LOAD_CONFIG(self, raw_config: dict[str, Any] | None = None) -> dict[str, Any]:
        return self.loadConfig(raw_config)
    
    @abstractmethod
    async def pre_loop(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def loop(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    async def post_loop(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def loadConfig(self, raw_config: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError

    '''roblox shortcuts'''
    def activateRoblox(self):
        roblox.activate_roblox_window(other=self)

    def terminateRoblox(self):
        roblox.terminate_roblox()

    def isRobloxFocused(self) -> bool:
        return roblox.is_roblox_focused()

    def closeRobloxChat(self,force:bool=False):
        if self._tracker is not None:
            self._tracker.close_chat_if_open(force)

    '''callbacks for hotkeys'''
    def add_callback_start_hotkey(self, func:Callable[..., Any], *args, **kwargs):
        if callable(func):
            if self.RESTRICT_CALLBACK_DUPLICATES:
                if not any(callback[0] is func and callback[1] == args and callback[2] == kwargs for callback in self._hotkey_start_callbacks):
                    self._hotkey_start_callbacks.append((func,args,kwargs))
            else: self._hotkey_start_callbacks.append((func,args,kwargs))
        return self

    def add_callback_stop_hotkey(self, func:Callable[..., Any], *args, **kwargs):
        if callable(func):
            if self.RESTRICT_CALLBACK_DUPLICATES:
                if not any(callback[0] is func and callback[1] == args and callback[2] == kwargs for callback in self._hotkey_stop_callbacks):
                    self._hotkey_stop_callbacks.append((func,args,kwargs))
            else: self._hotkey_stop_callbacks.append((func,args,kwargs))
        return self
    
    def _run_callbacks_start_hotkey(self, verbose:bool=False):
        className = self.getClassName()
        for func,args,kwargs in tuple(self._hotkey_start_callbacks):
            try:
                if(verbose):print(f'[{className}.{func.__name__}] Callback Started')
                func(*args,**kwargs)
                if(verbose):print(f'[{className}.{func.__name__}] Callback Ended')
            except Exception as e:
                print(f'[{className}.{func.__name__}] Macro Start callback failed: {e}')
        if(verbose):print(f'[{className}] Macro Start callbacks DONE')

    def _run_callbacks_stop_hotkey(self, verbose:bool=False):
        className = self.getClassName()
        for func,args,kwargs in tuple(self._hotkey_stop_callbacks):
            try:
                if(verbose):print(f'[{className}.{func.__name__}] Callback Started')
                func(*args,**kwargs)
                if(verbose):print(f'[{className}.{func.__name__}] Callback Ended')
            except Exception as e:
                print(f'[{className}.{func.__name__}] Macro Stop callback failed: {e}')
        if(verbose):print(f'[{className}] Macro Stop callbacks DONE')

    @staticmethod
    def sleep_interruptible(_should_continue:bool, _can_run:bool, seconds: float, poll: float = 0.02) -> bool:
        end = time.monotonic() + max(0.0, float(seconds))
        while time.monotonic() < end:
            if not _should_continue or not _can_run:
                return False
            remaining = end - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(min(poll, remaining))
        return _should_continue and _can_run

    @staticmethod
    def coerce_point(raw: list[int], fallback: list[int]) -> tuple[int, int]:
        if not isinstance(raw, (list, tuple)) or len(raw) < 2:
            return fallback[0], fallback[1]
        try:
            return int(raw[0]), int(raw[1])
        except Exception:
            return fallback[0], fallback[1]

    @staticmethod
    def coerce_region(raw: Any, fallback: list[int]) -> tuple[int, int, int, int]:
        if not isinstance(raw, (list, tuple)) or len(raw) < 4:
            return fallback[0], fallback[1], fallback[2], fallback[3]
        try:
            x = int(raw[0])
            y = int(raw[1])
            w = max(1, int(raw[2]))
            h = max(1, int(raw[3]))
            return x, y, w, h
        except Exception:
            return fallback[0], fallback[1], fallback[2], fallback[3]

    @staticmethod
    def coerce_int(raw: Any, fallback: int, min_value: int, max_value: int) -> int:
        try:
            value = int(raw)
            if value < min_value:
                return min_value
            if value > max_value:
                return max_value
            return value
        except Exception:
            return fallback

    @staticmethod
    def coerce_float(raw: Any, fallback: float, min_value: float, max_value: float) -> float:
        try:
            value = float(raw)
            if value < min_value:
                return min_value
            if value > max_value:
                return max_value
            return value
        except Exception:
            return fallback





if False:
    import random
    class temp(MACRO_BASE):
            
        def loadConfig(self, raw_config: dict[str, Any] | None = None) -> dict[str, Any]:
            raise NotImplementedError

        async def pre_loop(self, *args, **kwargs):
            print("LOOP OF PRE")
            while True:
                if random.randint(0,100000) == 1:
                    break
                await asyncio.sleep(0)

        
        async def loop(self, *args, **kwargs):
            print("LOOP OF MAIN")
            while True:
                if random.randint(0,100000) == 1:
                    break
                await asyncio.sleep(0)
        
        
        async def post_loop(self, *args, **kwargs):
            print("LOOP OF POST")
            while True:
                if random.randint(0,100000) == 1:
                    break
                await asyncio.sleep(0)



    async def main():
        temp2 = temp(None,None,True,True,True,True)
        def CALL_FUNCTION():
            print("CALLED A BASIC FUNCTION")

        def CALL_WITH_VARIABLES(value,special="FAILED"):
            print(value,special)

        #basic lambda call
        temp2.add_callback_start_hotkey(lambda:print("JUST PRINT SOMETHING WHEN DONE"))
        #lambda with variables
        temp2.add_callback_start_hotkey(lambda:CALL_WITH_VARIABLES("JUST PRINT SOMETHING WHEN DONE:","SOMETHING"))
        #basical function
        temp2.add_callback_stop_hotkey(CALL_FUNCTION)
        #function with additional variables and keyword variables
        temp2.add_callback_stop_hotkey(CALL_WITH_VARIABLES, "EXTREME STOP TEST", special="COMPLETE")

        #test
        temp2._run_callbacks_start_hotkey()
        test = await temp2.call_loop_test()
        while not (test.done() and not test.cancelling()):
            rand_select = random.randint(0,10)
            if rand_select == 0:
                await temp2.CANCEL()
                break
            await asyncio.sleep(0.1)
        await test
        temp2._run_callbacks_stop_hotkey()

    asyncio.run(main())