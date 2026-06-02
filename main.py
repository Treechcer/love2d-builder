import sys
import os
import re
import json

global inputs

pathStart = ""
inputs = {
    "--asepriteFolder" : "aseprite", #default currect folder, path is relative to where start the script
    "--outputFolder" : "assets", #destination of covertType files!
    "--convertType" : ".png", #type to which you convert
    "--test" : False, #just test value, will do NOTHING!!!
    "--asepriteCommand" : "aseprite",
    "--disableStdLog" : False
}
try:
    if not os.path.exists("love2d-builder/"):
        os.makedirs("love2d-builder/")
    log = open("love2d-builder/logger.txt", "a")
except:
    log = open("love2d-builder/logger.txt", "x")

def main():
    global pathStart
    try:
        with open("love2d-builder/config.json") as f:
            config = json.loads(f.read())
    except:
        writeLog("[CONFIG] ./love2d-builder/config.json not found. Using default values and values passed into the script.\n")
        cfg = open("love2d-builder/config.json", "w")
        cfg.write(json.dumps(inputs))
        cfg.close()
        config = inputs

    for i in config:
        if not re.match("--", i):
            i = "^--" + i
        inputs[i] = config[i]

    print(inputs["--asepriteCommand"])
    print(inputs)

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

    asespriteFiles = os.listdir(inputs["--asepriteFolder"])

    doFilesFromSource(inputs["--asepriteFolder"])

def doFilesFromSource(src):
    src = os.path.abspath(src)
    for i in os.listdir(src):
        if not os.path.isfile(os.path.abspath(src + "/" + i)):
            doFilesFromSource(src + "/" + i)
        else:
            fName, fExtension = os.path.splitext(i)
            if fExtension != ".aseprite" and fExtension != ".ase":
                writeLog("[INCORRECT FILE] incorrect file has been tried and is skipped'" + os.path.abspath(src + "/" + i) + "'\n")
                continue
            pathToNewFile = re.sub("/" + inputs["--asepriteFolder"] + "/", "/" + inputs["--outputFolder"] + "/", src)
            cmd = inputs["--asepriteCommand"] + " -b " + os.path.abspath(src + "/" + i) + " --save-as " + pathToNewFile + "/" + re.sub("\\.aseprite",inputs["--convertType"],i)
            os.system(cmd)
            writeLog(f"[FILE EXPORT] exported file with commad '{cmd}'\n")

def writeLog(message):
    log.write(message)
    if not inputs["--disableStdLog"]:
        print(message)

if __name__ == "__main__":
    main()

log.close()