# Influencer-Stats

A robust system for monitoring and reporting changes in Influencer’s YouTube playlist statistics.

Project Description:

Users can get an update about changes in their favourite youtuber's statists (views, likes and comments) as a telegram notification. The project uses pyspark for data managent and producses data to a kafka service which inturn triggers an aleart when there is a significant spike in the playlist's stats through telegram bots.

Project Screen Shot(s)
Example:

<img width="1069" alt="Screenshot 2023-09-11 at 5 38 30 PM" src="https://github.com/sujayk96/Influencer-Stats/assets/17350129/870b5063-9b4d-4c70-be72-16b091b53aae">

Above is a simple example where telegram bot sent out notifications with the name of the video in TISS playlist who's views cahnged from the last script run.


Installation and Setup Instructions
Example:
Clone down this repository. You will need to create a virtual env. I have created a pip virtual env but also used conda packages in it. Recommended to just create and use one.

Installation:

pip install requirement.txt

Set up API:

Get your youtube api credentials and paste it in the config file
Create an account on confluent.io for setting up a Kafka server and paste the credentials in config flie. 
Note: The API keys used in this project's code are expired. 

Running the code:

python watcher.py


I notice numerous influences today, and YouTube stands out as a massive platform for them. If you've ever uploaded videos on YouTube, you can access their analytics framework. However, if you're a brand seeking influencers to collaborate with based on their content performance, you'll need to individually examine the statistics of each video or playlist. To address this issue, I've developed a prototype to gather the statistics of YouTube playlists or videos collectively and transmit them to a Kafka server, which can then deliver the data and insights in various formats to your fingertips. This project provided me with a valuable learning experience in the realm of real-time data streaming and the utilization of tools like Kafka.

At the end of the day, the technologies used in this project are python, pyspark and kafka.

