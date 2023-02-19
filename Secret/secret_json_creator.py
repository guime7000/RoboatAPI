import json
import os

"""
Creates the JSON file for very ultra basic authentification...
"""

secretDirectoryPath = os.getenv("SECRET_DIRECTORY_PATH", "./Secret/")

dico = {"user1": "pwd1", "user2": "pwd2"}

os.makedirs(secretDirectoryPath, exist_ok=True)
filePath = os.path.join(secretDirectoryPath, "secret.JSON")

with open(filePath, "w") as outFIle:
    json.dump(dico, outFIle, indent=2)
