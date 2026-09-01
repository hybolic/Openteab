from __future__ import annotations

from openteab.globals import openteab, FROM_PATH, join_path
from datetime import datetime # do not remove or del used in print
import atexit;

LOG_DIR = FROM_PATH(openteab.top_directory, "logs")
LOG_FILE = open(join_path(LOG_DIR, "latest.log"),"w",encoding="utf-8")
python_print = print #for when we replace python base print with our logging one

#function that runs on python close
def onPythonClose():
    #flush and close log file
    LOG_FILE.flush()
    LOG_FILE.close()

# #register event
atexit.register(onPythonClose)

#reroute for logging

#temp quick print stuff
def print(*args, **kwargs):
    log_type = kwargs.pop("type", "PRINT")
    sep = kwargs.pop("sep", " ")
    end = kwargs.pop("end", "\n")
    message = sep.join(map(str, args))
    prefix = f"[{datetime.now():%d-%m-%Y %H:%M:%S}] [{log_type}] "
    python_print(prefix + message, end=end)
    LOG_FILE.write(prefix + message + end)
    return None
def print_exception(*args,**kwargs):kwargs["type"] = "EXCEPTION"; print(*args, **kwargs)
def print_log(*args,**kwargs): kwargs["type"] = "LOG"; print(*args, **kwargs)

print("Log Opened!", type="INIT")

def PreLaunch():
    import sys
    from importlib.metadata     import version, PackageNotFoundError
    from packaging.version      import Version
    from packaging.requirements import Requirement
    from subprocess             import run, PIPE
    from venv   import EnvBuilder
    from gzip   import decompress
    from base64 import b64decode
    from re import match, sub
    from shutil import copyfile
    from os.path import exists, abspath, dirname
    from os import makedirs, remove
    from urllib.request import urlretrieve;


    ### PRE-INIT

    #### STATIC DEFINITIONS ####
    retry = 0 # used for import tester
    WORKING_DIR       = abspath(dirname(sys.argv[0]))
    virtual_dir_abs   = "'"+openteab.venv+"'"
    requirements_path = ".\\requirements.txt"

    #required!
    node_js_version = "24.20.0"

    ### VIRTUAL ENVORIMENT ###

    def requirements_installed(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as lines:
            for line in lines:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                requirement = Requirement(line)
                try:
                    installed = version(requirement.name)
                except PackageNotFoundError:
                    return False
                if requirement.specifier and installed not in requirement.specifier:
                    return False
        return True

    def active_venv():

        #script location
        activatorpy = openteab.venv_activate_this
        activator   = openteab.venv_activate
        
        #enter virtual enviroment
        activator_command = activator + " & "
        
        #upgrade pip
        UpgradePip = (
            "" + activator_command +
            # upgrade pip
            "" + openteab.python_exe + " -m pip install --upgrade pip" )
        
        #install requirements.txt
        InstallRequirements = (
            #enter virtual enviroment
            "" + activator_command +
            #install requirements
            "" + openteab.pip_exe + " install --no-input -r " + requirements_path)
        
        #check if we are in an venv if not we make and enter one. this keeps the main python install clean
        if not (sys.prefix != (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix)) or not exists(openteab.venv + "/pyvenv.cfg"):
            print_log("FORCING VIRTUAL ENVIROMENT")
            
            #check if path exists
            if not (exists(openteab.venv) and exists(openteab.venv + "/pyvenv.cfg")):
                #build venv
                virtual = EnvBuilder(with_pip=True)
                virtual.create(env_dir=openteab.venv)
            
            #if we do not have a copy of the script locally we make one
            if not exists(activatorpy):
                #TODO: grab copy of activate script from github if its not avalible on system
                #local version
                with open(activatorpy, "w") as activate_filepy:
                    activate_filepy.write(decompress(b64decode("H4sIAAAAAAAC/z1RwW7jIBC9+yt8G2gcpN4qIw45VNqVut2om+3FtSxsjx0SBxBDV83fF5xtT7wZ5vHmPabgLqWj0ly8C7H0Oh5LTaWv0P4zwdl"
                                                            "cmCq3CX0uSP4fJRMxN44VXSmDWS5qFnm0iOFaD8oL3VOuWddNZsGu4wV+DOhj+awv+BiCC5l4rp2C8G79FWTQhrDcEWGIxtl1hl1oVjCZj68tYe"
                                                            "M2IG+HSMRuFckSHPiUHZ0LneRHE2wSYgOXvdJNvV3QMvgzBOMjAd/et/KkYL87/ABpmlOrSJycsazR1Z0RM0Z2qgC4IL+YyIi3XFoFrz9fDn93T"
                                                            "93j82um2Vb1+dhAt3/5/Wt/gFYBJGde9JpwXaDnElUWv+XDiyndT6WxIMTbk+nfcphbr4eznpHgW7Aek4uAelkN+tt2upo4l0ehxzHTkkk2ihEH"
                                                            "NyKD9zhtH4CbCQCXlOTIi6WpW7U0WLebBLGV8/pk5wOmTPOXrUB+AdV/AqZng0UVAgAA")).decode())
            if not exists(activator):
                #TODO: grab copy of activate script from github if its not avalible on system
                #local version
                with open(activator, "w") as activate_file:
                    activate_file.write(decompress("H4sIAAAAAAAA/52SUWuDMBDH3/0UN+1D++CKe+xwYKlgoVVpbGEbQ6RGDJS0aJSx0u8+1NTGpboxXyR3/+R+d/ePcbRnpIwYhvEEzgoAAEngHXQK"
                                                "6ugceqtFuFtugq21Cn0rcGb6RYUPeAaWYlqrq6/KmH3yVoU/T8eM1eI2VtAcM5Du1fmEDOO8Bo7nOt7a7oFq8zJa56oE2GYHMbuqhCg/aecWaual"
                                                "H3nkDTnhzt6gpefeZ06jPAU9g6cXmMa4nNLicPjTLJDRMwRkyN03YqltZAz2y9OcpFFck7a7u/E9VHgNjwkqPdIY5ywrKp/hO4jNS3oCcevFa6GL"
                                                "cotB9yFFKG1qmiYcNU1TeE8in2QyUx1VP1XhB0E8RfuMnFg+4wrRusIOhizYYxZTuiaMU/BUQnihr6qQgBYulsiar+zQ33hrP/itcLN/ceV1aPxY"
                                                "YlpOoJsSnNDW/4+V79o4Id8Ru3CgbQQAAA==").decode())
                with open(activator, "r") as text_file:
                    all_lines = text_file.readlines()
                    text_file.close()
                    for index, line in enumerate(all_lines):
                        if match("VIRTUAL_ENV=\#\#\#VIRTUAL_ENV\#\#\#", line):
                            all_lines[index] = sub("\#\#\#VIRTUAL_ENV\#\#\#", "'" + virtual_dir_abs + "'", line)
                            break
                with open(activator, "w") as text_file:
                    text_file.writelines(all_lines)
            
                #we no longer need to use these so to save memory get rid of them
            
            #open a %CWD%\\%virtual_dir%\\Scripts\\activate_this.py as a TextIOWrapper
            with open(openteab.venv_activate_this) as f:
                # read file and compile the code for exec and execute it in script
                exec(compile(f.read(), activatorpy, 'exec'), dict(__file__=activatorpy))

        #check if we have all required python libs
        if not requirements_installed(requirements_path):
            required_pip_ver = Version("26.2.1")
            try:
                currpip = Version(version("pip"))
            except PackageNotFoundError:
                currpip = Version("0.0.0")
            if currpip < required_pip_ver:
                try:
                    print_log("this might take a while!")
                    print_log("running command: '" + UpgradePip + "'")
                    run(UpgradePip, cwd=WORKING_DIR, shell=True, check=True, encoding="UTF-8")
                except Exception as e:
                    print_exception(e)
            print_log("install requirements")
            #run command and output to print
            try:
                print_log("running command: '" + InstallRequirements + "'")
                run(InstallRequirements, cwd=WORKING_DIR, shell=True, check=True, encoding="UTF-8")
            except Exception as exception:
                print_exception(exception)
        #final check if we are now in a virtual enviroment! tell user!
        if not sys.prefix != (getattr(sys, "base_prefix", None) or getattr(sys, "real_prefix", None) or sys.prefix):
            #throw error message
            print_exception("WE ARE NOT IN A VIRTUAL ENVIROMENT PLEASE CONTANCT THE DEVS!")
            exit()
        else:
            print_log("WE ARE IN A VIRTUAL ENVIROMENT")
    active_venv()

    #### END OF VENV LOADER ###
    
    #TODO: if frontend not built, run this lower area!
    #### NODE.js ####

    #TODO: add system os checks
    system_os = "WINDOWS"

    #windows
    nodejs_url_msi = "https://nodejs.org/dist/v" + node_js_version + "/node-v" + node_js_version + "-x64.msi"

    #macos
    nodejs_url_pkg = "https://nodejs.org/dist/v" + node_js_version + "/node-v" + node_js_version + ".pkg"

    #not suppported by roblox
    #linux
    nodejs_url_xz  = "https://nodejs.org/dist/v" + node_js_version + "/node-v" + node_js_version + "-linux-x64.tar.xz"

    node_version_command = ["node", "--version"]

    def download_file(url, save:str):
        #make temp downloads directory
        if not exists(openteab.top_directory + "\\temp\\"):
            makedirs(openteab.top_directory + "\\temp\\")
        temp_filepath = openteab.top_directory + "\\temp\\file.tmp"
        if exists(temp_filepath):
            remove(temp_filepath)
        #download file to temp directory and filename
        
        urlretrieve(url, temp_filepath);
        if exists(save): copyfile(save, save + ".bak")
        copyfile(temp_filepath, save)


    def getNodeVersion():
        try:
            process = run(node_version_command, cwd=WORKING_DIR, check=True, encoding="UTF-8", stdout=PIPE)
            return process.stdout.rstrip("\n").lstrip("v")
        except:
            return "v0.0.0"
        
    NodeVersion = getNodeVersion()
    print_log(NodeVersion + " >= v24.20.0 ? " + str(Version(NodeVersion) >= Version(node_js_version)))

    install_file = None
    install_new = None

    if not Version(NodeVersion) >= Version(node_js_version):
        if system_os == "WINDOWS":
            install_file = openteab.top_directory + "\\temp\\node-v" + node_js_version + "-x64.msi"
            download_file(nodejs_url_msi, install_file)
            install_new = ["msiexec.exe","/i",str(install_file),"/passive","/norestart"]
            run(install_new, cwd=WORKING_DIR, check=True)

    NodeVersion = getNodeVersion()
    if Version(NodeVersion) >= Version(node_js_version):
        print_log("Node Installed!")
    else:
        print_exception("Version failed to update or install!")
        exit()

    #### END NODE.js ####
    
    #### NPM ####
    npm_install = ["npm.cmd","install"]
    npm_build = ["npm.cmd","run","build"]

    #TODO: Add check for npm install requirements
    # run(npm_install, cwd=openteab.frontend, check=True)
    #TODO: Build frontend
    run(npm_build,   cwd=openteab.frontend, check=True)
    print_log("PreLanch Done!")

#### END NPM ####
PreLaunch()
del PreLaunch