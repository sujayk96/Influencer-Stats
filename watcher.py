

import logging
import requests
from config import config
import json
from pprint import pformat
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka import SerializingProducer

def fetch_youtube_video_page(api_key, youtube_playlist_id, page_token=None):
	response =requests.get("https://www.googleapis.com/youtube/v3/playlistItems", params={
		"key": api_key,
		"playlistId": youtube_playlist_id,
		"part": "contentDetails",
		"pageToken": page_token
		})
	payload = json.loads(response.text) 
	return payload

def fetch_youtube_playlist_content(api_key, youtube_playlist_id, page_token=None):

	payload = fetch_youtube_video_page(api_key, youtube_playlist_id, page_token)

	yield from payload["items"]
	next_page_token = payload.get("nextPageToken")
	if next_page_token is not None:
		yield from fetch_youtube_playlist_content(api_key, youtube_playlist_id, next_page_token)


def fetch_youtube_video(api_key, youtube_video_id, page_token=None):
	response =requests.get("https://www.googleapis.com/youtube/v3/videos", params={
		"key": api_key,
		"id": youtube_video_id,
		"part": "snippet,statistics",
		"pageToken": page_token
		})
	payload = json.loads(response.text) 
	return payload

def fetch_youtube_video_content(api_key, youtube_video_id, page_token=None):

	payload = fetch_youtube_video(api_key, youtube_video_id, page_token)

	yield from payload["items"]
	next_page_token = payload.get("nextPageToken")
	if next_page_token is not None:
		yield from fetch_youtube_video_content(api_key, youtube_video_id, next_page_token)	


def summarize_video(video):
	return {
	"video_id": video["id"],
	"title": video["snippet"]["title"],
	"views": video["statistics"]["viewCount"],
	"likes": video["statistics"]["likeCount"],
	"comment": video["statistics"]["commentCount"],
	}

def on_delivery(err, record):
	pass

def main():
	logging.info("START")
	schema_registry_client = SchemaRegistryClient(config["schema_registry"])
	youtube_videos_value_schema = schema_registry_client.get_latest_version("youtube_videos-value")


	kafka_config = config["kafka"] | {
	"key.serializer": StringSerializer(),
	"value.serializer": AvroSerializer(schema_registry_client,youtube_videos_value_schema.schema.schema_str)
	}
	producer = SerializingProducer(kafka_config)
	api_key = config["google_api_key"]
	youtube_playlist_id = config["youtube_playlist_id"]
	for vid_details in fetch_youtube_playlist_content(api_key, youtube_playlist_id):
		video_id = vid_details["contentDetails"]["videoId"]
		print("video_id for this iteration", video_id )
		for video in fetch_youtube_video_content(api_key, video_id):
			logging.info(pformat(summarize_video(video)))

			producer.produce(
				topic = "youtube_videos",
				key = "Mahesh Dalle",
				value = {
					"VIDEO_ID": video_id,
					"TITLE": video["snippet"]["title"],
					"VIEWS": int(video["statistics"]["viewCount"]),
					"COMMENTS": int(video["statistics"]["commentCount"]),
					"LIKES": int(video["statistics"]["likeCount"]),
					
					},
				on_delivery = on_delivery

				)
	producer.flush()

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	main()