# RoboatAPI
Simple python fastAPI to retrieve informations of Virtual Regatta's Roboats for the route du rhum 2022

# History
After working on the development of my own bot for Virtual regatta IRoboat Challenge, I unfortunately didn't qualify for the Route du Rhum 2022..

But I wanted to be able to follow my ancient opponents, who qualified, during their Route du Rhum 2022...

So I built this quite rustic API to retrieve Roboats informations and visualize their position on a folium map...

See this simple project as a discovery of fastAPI...

# Requirements

Nothing more than python 3 and fastAPI

My API's running using uvicorn...but choose the asgi server you prefer

# How is it working ?

First of all, you'll need to execute the 2 scripts in the Tools directory to initalize your folders :
  * positionFiles_initial_creator.py will create the default files for each Roboat
  * archiveFiles_initial_creator.py will create the files for Archiving position
 

