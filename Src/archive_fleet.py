import json
import logging
import os
import time

"""
Concatenates all complete Roboats positions files to have fleet history over the duration of the race

script ran via a crontab task

"""
logFilePath = os.getenv("LOG_FILE_PATH", "Logs/fleetArchived.log")
logFormat = "%(asctime)s %(message)s"

logging.basicConfig(
    filename=logFilePath, encoding="utf-8", level=logging.INFO, format=logFormat
)
archiveDirectoryPath = os.getenv("ARCHIVE_DIRECTORY_PATH", "Archives/")

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
    archivePositionFile = os.path.join(archiveDirectoryPath, inName + "_Arch.JSON")

    with open(archivePositionFile, "r") as outJsonFile:
        response = json.load(outJsonFile)

    fleetDict[inName] = response

with open(os.path.join(archiveDirectoryPath, "fleet_Arch.JSON"), "w") as fleetFile:
    json.dump(fleetDict, fleetFile, indent=2)

logging.info("Fleet correctly Archived")
