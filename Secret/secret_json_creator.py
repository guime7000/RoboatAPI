import json
import os

"""
Creates the JSON file for very ultra basic authentification...
"""

secretDirectoryPath = "/somewhere_over_the_rainbow/Secret/"

dico = {"user1": "pwd1", "user2": "pwd2"}

filePath = os.path.join(secretDirectoryPath, "secret.JSON")

with open(filePath, "w") as outFIle:
    json.dump(dico, outFIle, indent=2)
