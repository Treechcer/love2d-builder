import sys
import os
import re
import json
import platform
import subprocess
import time
import math
import zipfile
import requests

global inputs, processes, loveFiles, loveData

#loveFiles = {
#    "win" : [
#        "love-win64",
#        "love-win32"
#    ],
#    "linux" : [
#
#    ],
#    "macos" : [
#
#    ],
#    "android" : [
#
#    ]
#}

def getDefaultLoveData():
    return {
            "buildData" : {
                "folderIgnore" : [
                    "aseprite"
                ]
            },
            "windows32": {
                "version": 11.5,
                "backupVersion": None,
                "folder" : "love-win32",
                "build" : True,
                "lovePlatformName" : "win32"
            },
            "windows64": {
                "version": 11.5,
                "backupVersion": None,
                "folder" : "love-win64",
                "build" : True,
                "lovePlatformName" : "win64"
            },
            "linux": {
                "version": 11.5,
                "backupVersion": None,
                "folder" : "-----",
                "build" : False,
                "lovePlatformName" : None
            },
            "macos": {
                "version": 11.5,
                "backupVersion": None,
                "folder" : "-----",
                "build" : False,
                "lovePlatformName" : None
            },
            "android": {
                "version": 11.5,
                "backupVersion": None,
                "folder" : "-----",
                "build" : False,
                "lovePlatformName" : None
            }
        }

loveData = getDefaultLoveData()

pathStart = ""
inputs = {
    "--asepriteFolder" : "aseprite", #default currect folder, path is relative to where start the script
    "--outputFolder" : "assets", #destination of covertType files!
    "--convertType" : ".png", #type to which you convert
    "--test" : False, #just test value, will do NOTHING!!!
    "--asepriteCommand" : "aseprite",
    "--disableStdLog" : False,
    "--mode" : "imageConvert",
    "--gameName" : "nameNotSet",
    "--loveFilesPath" : "not-set", #FOR love.exe!!
    "--downloadAuto" : False, #auto downloads the love files if missing
}

processes = []

machineOs = platform.system().lower()

try:
    if not os.path.exists("love2d-builder/"):
        os.makedirs("love2d-builder/")
    log = open("love2d-builder/logger.txt", "a")
except:
    log = open("love2d-builder/logger.txt", "x")

slash = ""

if machineOs == "linux" or os == "darwin":
    slash = "/"
else:
    slash = "\\"

def main():
    global pathStart

    try:
        with open("love2d-builder/love-data.json") as f:
            loveData = json.loads(f.read())
    except:
        writeLog("[Love Data] ./love2d-builder/love-data.json not found. Using default values and values.")
        cfg = open("love2d-builder/love-data.json", "w")
        cfg.write(json.dumps(getDefaultLoveData(), indent=4))
        cfg.close()

    try:
        with open("love2d-builder/config.json") as f:
            config = json.loads(f.read())
    except:
        writeLog("[CONFIG] ./love2d-builder/config.json not found. Using default values and values passed into the script.")
        cfg = open("love2d-builder/config.json", "w")
        cfg.write(json.dumps(inputs, indent=4))
        cfg.close()
        config = inputs

    for i in config:
        if not re.match("--", i):
            i = "^--" + i
        inputs[i] = config[i]

    #print(inputs["--asepriteCommand"])
    #print(inputs)

    tab = sys.argv
    tab = tab[1::1]
    for i in range(0, len(tab), 2):
        #inputs[tab[i]] = inputs[tab[i+1]]
        #print(inputs[tab[i]], i)
        if type(inputs[tab[i]]) == bool:
            inputs[tab[i]] = not inputs[tab[i]]
            i -= 1
        else:
            inputs[tab[i]] = tab[i+1]

    pathStart = re.sub(f"{inputs["--asepriteFolder"]}$", "", f"{os.path.abspath(inputs["--asepriteFolder"])}")
    
    #print(os.listdir(inputs["--asepriteFolder"]))
    #print(os.listdir(inputs["--outputFolder"]))

    #asespriteFiles = os.listdir(inputs["--asepriteFolder"])

    if inputs["--mode"] == "imageConvert":
        doFilesFromSource(inputs["--asepriteFolder"])
        checkProcesses()
    elif inputs["--mode"] == "build":
        build()

def checkFile(file, path):
    if not os.path.isdir(path + "/" + file):
        try:
            with zipfile.ZipFile(path + "/" + file + ".zip", "r") as zipr:
                zipr.extractall(path)
                name = zipr.namelist()[0].split("/")[0]

                #print(os.path.abspath(os.path.join(path + "/" + file)), os.path.abspath(os.path.join(path + "/" + name)))
                os.rename(os.path.abspath(os.path.join(path + "/" + name)), os.path.abspath(os.path.join(path + "/" + file)))
        except:
            return False
        
    return True

def checkLoveFiles():
    folder = inputs["--loveFilesPath"] if inputs["--loveFilesPath"] != "not-set" else ("love2d-builder", writeLog("[Love Files] Love folders path was not set, looking into ./love2d-builder/love___/"))[0]
    inputs["--loveFilesPath"] = folder

    for key in loveData:
        if key == "buildData":
            continue

        platform = loveData[key]
        if not platform["build"]:
            continue

        name = platform["folder"]

        if checkFile(name, folder):
            #BUILD GAME!!!
            pass
        else:
            writeLog(f"[Love Files] not found '{name}' in directory '{folder}', do you want to download them?")
            
            userInput = "y" if inputs["--downloadAuto"] else ""

            while userInput != "y" and userInput != "n":
                userInput = input("Do you want to download love folder Files? y/n ")
            
            if userInput == "y":
                retry = True
                while retry:
                    url = f"https://github.com/love2d/love/releases/download/{platform['version']}/love-{platform['version']}-{platform['lovePlatformName']}.zip"
                    response = requests.get(url, stream=True)
                    if response.status_code == 200:
                        with open(f"{folder}/love-{platform['lovePlatformName']}.zip", "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        
                        retry = False
                    else:
                        #TODO: TEST THIS PART!!

                        writeLog(f"[Download error], '{response.status_code}', do you want to try it again?")
                        retryInput = ""
                        while retryInput != "y" and retryInput != "n":
                            retryInput = input("Do you want to try to download love folder Files? y/n ")
                        
                        retry = True if retryInput == "y" else False
                        
                    print(folder, f"love-{platform['lovePlatformName']}.zip")
                    if not checkFile(name, folder):
                        writeLog("[Unexpected Error] file was downloaded but not found?")

def buildWin():
    osType = platform.system().lower()

    cmd = ""

    if osType == "linux" or osType == "darwin":
        cmd = f"zip -9 -r '{inputs["--gameName"]}.love' ."
    elif osType == "win32" or osType == "windows":
        items = []
        for item in os.listdir():
            #print(item)
            if item == "love2d-builder" or item in loveData["buildData"]["folderIgnore"]:
                writeLog(f"[File Ignore] {item}")
                continue
            items.append(item)
        
        cmd = f"powershell -Command Compress-Archive -Path {", ".join(items)} -DestinationPath '.\\{inputs["--gameName"]}.love'"
    else:
        writeLog(f"[UNKNOWN OS] OS was not identified '{osType}'")
        exit()
    
    os.system(cmd)
    writeLog(f"[CMD EXECUTE] executed command '{cmd}'")

    if osType == "linux" or osType == "darwin":
        cmd = f"cat '{inputs["--loveFilesPath"]}' '{inputs["--gameName"]}.love' > 'Win-{inputs["--gameName"]}.exe'"
    elif osType == "win32" or osType == "windows":
        cmd = f"cmd /c copy /b ./{inputs["--loveFilesPath"]}/love-win64/love.exe+{inputs["--gameName"]}.love Win-{inputs["--gameName"]}.exe"
    
    os.system(cmd)
    writeLog(f"[CMD EXECUTE] executed command '{cmd}'")

def build():
    #TODO: check love-data and build acordingly to what is there, for now I'll make it build everything but whatever for now
    checkLoveFiles()
    buildWin()

def doFilesFromSource(src):
    src = os.path.abspath(src)
    for i in os.listdir(src):
        if not os.path.isfile(os.path.abspath(src + "/" + i)):
            doFilesFromSource(src + "/" + i)
        else:
            fName, fExtension = os.path.splitext(i)
            if fExtension != ".aseprite" and fExtension != ".ase":
                writeLog("[INCORRECT FILE] incorrect file has been tried and is skipped'" + os.path.abspath(src + "/" + i) + "'")
                continue
            pathToNewFile = src.replace(slash + inputs["--asepriteFolder"] + slash, slash + inputs["--outputFolder"] + slash)
            cmd = "\"" + inputs["--asepriteCommand"] + "\" -b \"" + os.path.abspath(src + "/" + i) + "\" --save-as \"" + pathToNewFile + "/" + re.sub("\\.aseprite",inputs["--convertType"] + "\"",i)
            processes.append(subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))

def checkProcesses():
    lastNumProcesses = len(processes)
    maxProcess = lastNumProcesses
    while len(processes) > 0:
        for i, process in enumerate(processes[:], 1):
            if not process.poll() is None:
                processes.remove(process)
        
        if lastNumProcesses != len(processes):
            lastNumProcesses = len(processes)
            percent = math.floor(100 - (lastNumProcesses / maxProcess * 100))
            charBar = "█" * math.floor(percent/10) + " " * (10 - math.floor(percent/10))
            bar = f"{percent}% [{charBar}]"
            print(f"\rProcess remaining: {lastNumProcesses}      |      {bar}              ", end="")
            sys.stdout.flush()
        
        time.sleep(1)

def writeLog(message):
    if message[-1] != "\n":
        message += "\n"
    log.write(message)
    if not inputs["--disableStdLog"]:
        print(message)

if __name__ == "__main__":
    main()

log.close()