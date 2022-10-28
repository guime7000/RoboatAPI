# RoboatAPI
Simple python fastAPI to retrieve informations of Virtual Regatta's Roboats for the route du rhum 2022

# History
After working on the development of my own bot for Virtual regatta IRoboat Challenge, I unfortunately didn't qualify for the Route du Rhum 2022..

But I wanted to be able to follow my ancient opponents, who qualified, during their Route du Rhum 2022...

So I built this quite rustic API to retrieve Roboats informations and visualize their position on a folium map...

See this simple project as a discovery of fastAPI...Probably a lot to do to get a cleaner solution....but i works

# Requirements

Nothing more than python 3 and fastAPI.

No database needed as everything is working on file exchanges.

My API's running using uvicorn...but choose the asgi server you prefer.

# How is it working ?

First of all, you'll need to execute the 2 scripts in the Tools directory to initalize your folders :
  * positionFiles_initial_creator.py will create the default files for each Roboat
  * archiveFiles_initial_creator.py will create the files for Archiving position

Second : Be sure to execute the secret_json_creator.py (after editing it) in the Secret directory. This will generate a JSON file used to quite rusticaly secure the POST method access of the API.

I know this is not very secure, I know there are other solutions (jwt, oAuth..) but I'm discovering fastAPI and the timing for putting all this together is quite short...

Third : Run the roboatAPI.py with your favorite asgi server...(after editing the Paths variables in the file ;-)

Last but not least : Run 2 crontab tasks for:
 - archive_fleet.py : archives history of all Roboats informations since the beginning of the race and creates a global fleet file containing all archived Roboats infos
 - concatenate_fleet.py : periodically generates the fleet file with the last known Roboats informations

# TO DO

* really secure access to POST method with a really secure solution ;-)
* work with a config file...

