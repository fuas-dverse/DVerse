# Prototype Sprint 1
This directory contains the first ever made prototype of the 'Dverse' project. The primary purpose of this prototype is to demonstrate the foundational concepts envisioned for the end goal of this project.


## Context
The goal of this sprint was as followed: 
- "Create a very basic prototype that shows agents communicating with each other in any way."


Previous sprints we have all been working on creating some small agents for example, a`Festival Information Agent`, a `YouTube Search Agent` or a`Google Search Agent`. We decided on which of these created agents we wanted to include in our first demo, those are the ones mentioned here above.


So the scenario for this prototype will be: "Getting information about a festival".


So then the big questions behind this prototype, how does it work and why is it only a demo and cant it be used for the final project?


### How does it work
First thing we have done to make this prototype work, is setup all the agents get a query and that they can return their data via a HTTP-POST call. After setting up the agents in this way, I dockerized all of the agents so that they can be started with a single docker compose file, then inside of this compose file, I setup a network where all these agents will be hooked into.


For this prototype we choose to create a predefined path that the data should flow. For booking a festival this flow is first getting data about a festival, then getting some after movies for inspiration about this festival and last the ticket links to this festival.


So the order of agents should be as followed, I gave all of them a specific port so that they can be easily identified. 
1. UI / Interface
	- `http://127.0.0.1:5003`
	- `http://websocket-server:5003/`
2. Festival Information Agent, 
	- `http://127.0.0.1:5000
	- `http://festival-information-agent:5000/`
3. YouTube Search Agent
	- `http://127.0.0.1:5001
	- `http://youtube-search-agent:5001/`
4. Google Search Agent
	-  `http://127.0.0.1:5002`
	- `http://google-search-agent:5002/`


Inside the UI I created a JSON object that looks something like:
```json
{  
    "query": user_input,  
    "origin": ORIGIN_URL,  
    "domains": [  
        FESTIVAL_AGENT_API_URL,  
        YOUTUBE_AGENT_API_URL,  
        GOOGLE_AGENT_API_URL  
    ]  
}
```

Where:
- `query`: The input or question from the user
- `origin`: The domain of the UI / interface
- `domains`: The ordered domains the query needs to travel through


After this I created a post request to sent this JSON to the first domain in the list, so FESTIVAL_AGENT_API_URL. Inside of this application it does its logic and adds it the JSON data under a new key called `responses`.


When processed in the first agent, I made a function that checks for the next domain in the list after the current one and sends the data to the new domain this continues till the end of the domain, when it will send the data back to `origin`.


Once the data is at origin, it will be sent from a Python script to JavaScript via web sockets and the UI will be updated.


### Why does this need to change
While having our first scenario setup, this route will never work when having dynamic bots that wait for work, this is why our first prototype will not be the end result of our project.


## Setup Prototype
To run this prototype first clone the repository into a directory where you want to store it.
```console
git clone https://github.com/fuas-dverse/DVerse.git
```


After cloning it navigate to `docker-compose` file inside of the `Prototype 1` folder. Inside of this file change the following variables:
- OPENAI_API_KEY
	- https://platform.openai.com/api-keys
- MONGO_URI
	- https://www.mongodb.com/
- API_KEY (YouTube Data API v3)
	- https://console.cloud.google.com/apis


Before we go further we need to get the information to seed the database, for this we need to run the `FestivalInformationScrapper` which is located at [Scrapper](https://github.com/fuas-dverse/ticket-system-agent/tree/main/festival-information-agent/FestivalInformationScrapper), where we also needed the OPENAI_API_KEY and MONGO_URI inside of a .env file.


Once the variables are changed and the database is seeded you can start the docker client and run, to start the docker containers:
```console
docker-compose up
```


If everything works correctly, you should be able to go to [UI / Interface](http://127.0.0.1:5003) and see a UI pop up, here you can enter a query. This prototype is optimized based on something like the following question: `Give me only the name of one festival to go to in the summer!`.


After some time this will result in the UI changing with the gotten information from the three agents.