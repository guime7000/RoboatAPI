import json
import os

"""
Creates the initial JSON archive file for each roboat and fleet
"""

boatsDirectoryPath = os.getenv("BOATS_DIRECTORY_PATH", "./Boats/")


fleetList = [
    "groziboat",
    "axelair",
    "shapeshifters",
    "modiababord",
    "millesabords",
    "chatboatez",
    "echeneis",
    "totorson",
    "deepsink",
    "robotak",
    "fleet",
]

dico = {
    "ts": 0,
    "lat": 0,
    "lon": 0,
    "distanceToEnd": 0,
    "rank": 0,
    "speed": 0,
    "tws": 0,
    "twa": 0,
    "heading": 0,
}

for inName in fleetList:
    filedir = os.path.join(boatsDirectoryPath, inName)
    os.makedirs(filedir, exist_ok=True)

    filePath = os.path.join(filedir, inName + "_Arch.JSON")
    with open(filePath, "w+") as outFIle:
        json.dump([dico], outFIle, indent=2)
