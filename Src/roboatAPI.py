import json
import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

"""
Simple API to retrieve IRoboat positions during the Route du Rhum 2022 on virtual regatta

Each qualified boat sends:

last calculation timestamp,
latitude,
longitude,
distanceToEnd,
rank,
speed,
tws,
twa,
heading

A JSON file for each roboat and a JSON file containing all roboats data are then appended and
downloadable

POST /url/boat/position/ : API endpoint to send VR fastinfo call's response

GET /url/boat/<name of boat>  : to retrieve a JSON file containing one particular boat last known informations

GET /url/fleet : to retrieve a JSON file containing the last known informations of the fleet

GET /archives/<name of the boat> : to retrieve all the history (since the beginning of the race) of transmitted informations for each boat.
                                    If <name of the boat> is fleet, then all the history of the fleet is concatenated in a single (big) file


"""

boatsDirectoryPath = os.getenv("BOATS_DIRECTORY_PATH", "Boats/")
archiveDirectoryPath = os.getenv("ARCHIVE_DIRECTORY_PATH", "Archives/")
logsDirectoryPath = os.getenv("LOGS_DIRECTORY_PATH", "Logs/")
tempo = 300  # time delay between two possible posts in seconds

os.makedirs(archiveDirectoryPath, exist_ok=True)
os.makedirs(logsDirectoryPath, exist_ok=True)

# Log files config
logging.getLogger("").setLevel(logging.DEBUG)


def create_log_file(filename, level=logging.INFO, loggerNumber=""):
    handler = logging.FileHandler(filename)
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s %(levelname)-3s %(message)s")
    handler.setFormatter(formatter)
    logging.getLogger(loggerNumber).addHandler(handler)


create_log_file(os.path.join(logsDirectoryPath, "post.log"), logging.INFO, "post")
create_log_file(os.path.join(logsDirectoryPath, "fleet.log"), logging.INFO, "fleet")
create_log_file(os.path.join(logsDirectoryPath, "boat.log"), logging.INFO, "boat")
create_log_file(
    os.path.join(logsDirectoryPath, "archive.log"), logging.INFO, "archive.log"
)


# End of log files config


class BoatPos(BaseModel):
    inPwd: str
    inName: str
    inTs: int
    inLat: float
    inLon: float
    inDist: float
    inRank: int
    inSpeed: float
    inTws: float
    inTwa: float
    inHeading: float = 0.0


app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/boat/{inName}")
async def get_boat(inName: str):
    boatLogger = logging.getLogger("boat")
    positionFile = os.path.join(boatsDirectoryPath, inName, inName + ".JSON")

    with open(positionFile, "r") as outJsonFile:
        response = json.load(outJsonFile)

    boatLogger.info(f"GET for {inName}")

    return response


@app.get("/fleet")
async def get_fleet():
    fleetLogger = logging.getLogger("fleet")

    positionFile = os.path.join(boatsDirectoryPath, "fleet", "fleet.JSON")

    with open(positionFile, "r") as outJsonFile:
        response = json.load(outJsonFile)

    fleetLogger.info("GET for fleet")

    return response


@app.get("/archives/{inName}")
async def get_boat(inName: str):
    archiveLogger = logging.getLogger("archive")

    positionFile = os.path.join(archiveDirectoryPath, inName + "_Arch.JSON")

    with open(positionFile, "r") as outJsonFile:
        response = json.load(outJsonFile)

    archiveLogger.info(f"Archive GET for {inName}")

    return response


@app.post("/boat/position/")
async def position(boatInfos: BoatPos):
    """
    Gets :
        - inPwd : password
        - inName : Name of the boat (one of the 10 qualified roboats)
        - inTs : timsetamps corresponding to TsLastCalc on Virtual Regatta server
        - inLat : Latitude
        - inLon : Longitude
        - inDist : Distance To End
        - inRank : rank
        - inSpeed : boat speed
        - inTws : tws
        - inTwa : twa
        - inHeading : heading
    """
    postLogger = logging.getLogger("post")

    with open(
        "/a_secret_place_to_store_the_pwd_file/secret_containing_pwd_file.JSON", "r"
    ) as pwdf:
        pwd = json.load(pwdf)

    if pwd[boatInfos.inName] != boatInfos.inPwd:
        postLogger.info(f"[ERROR] : {boatInfos.inName} tried to connect but failed...")
        raise HTTPException(status_code=401, detail="Bad credential")

    else:
        archivePositionFile = os.path.join(
            archiveDirectoryPath, boatInfos.inName + "_Arch.JSON"
        )
        lastPositionFile = os.path.join(
            boatsDirectoryPath, boatInfos.inName, boatInfos.inName + ".JSON"
        )

        dico = {
            "ts": boatInfos.inTs,
            "lat": boatInfos.inLat,
            "lon": boatInfos.inLon,
            "distanceToEnd": boatInfos.inDist,
            "rank": boatInfos.inRank,
            "speed": boatInfos.inSpeed,
            "tws": boatInfos.inTws,
            "twa": boatInfos.inTwa,
            "heading": boatInfos.inHeading,
        }

        with open(lastPositionFile, "r") as timeCheckFile:
            lastPost = json.load(timeCheckFile)

        if (boatInfos.inTs - lastPost[0]["ts"]) < (tempo - 2):
            postLogger.info(
                f"[ERROR] : {boatInfos.inName} tried to post before the time delay of {tempo} seconds expired"
            )
            raise HTTPException(
                status_code=409,
                detail=f"POST frequency is too small (you can post only once every {tempo} seconds)",
            )

        updatedDict = []
        with open(archivePositionFile, "r") as inFile:
            updatedDict = json.load(inFile)

        updatedDict.append(dico)

        with open(archivePositionFile, "w") as outFile:
            json.dump(updatedDict, outFile, indent=2)

        with open(lastPositionFile, "w") as tmpOutFIle:
            json.dump([dico], tmpOutFIle, indent=2)

        postLogger.info(f"Post for {boatInfos.inName}")

        return {"Boat infos correctly uploaded"}
