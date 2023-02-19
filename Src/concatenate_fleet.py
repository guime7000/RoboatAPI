import json
import logging
import os
import time

"""
Concatenates last known roboats position in one JSON file for dash use

script launched periodically using a crontab task.

"""
logFilePath = "/home/tom/Api/Logs/fleetConcat.log"
logFormat = "%(asctime)s %(message)s"
logging.basicConfig(
    filename=logFilePath, encoding="utf-8", level=logging.INFO, format=logFormat
)

boatsDirectoryPath = os.getenv("BOATS_DIRECTORY_PATH", "Boats/")
fleetDirectoryPath = os.getenv("FLEET_DIRECTORY_PATH", "Boats/fleet")

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
]

fleetDict = {}
fleetDict["lastConcatTs"] = int(time.time())

for inName in fleetList:
    positionFile = os.path.join(boatsDirectoryPath, inName, inName + ".JSON")

    with open(positionFile, "r") as outJsonFile:
        response = json.load(outJsonFile)

    fleetDict[inName] = response

with open(os.path.join(fleetDirectoryPath, "fleet.JSON"), "w") as fleetFile:
    json.dump(fleetDict, fleetFile, indent=2)

logging.info("Fleet correctly concatenated")
