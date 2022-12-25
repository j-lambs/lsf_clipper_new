# importing necessary libraries
import os
import urllib.request, urllib.parse, urllib.error
import http.client
import urllib.request
import urllib.error
import http.client
import httplib2
import random
import time
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import socket

socket.setdefaulttimeout(30000)


# Authenticate with the Google API
# Replace the values in the following lines with your own values
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

# Get credentials
def get_authenticated_service():
	flow = InstalledAppFlow.from_client_secrets_file(
						CLIENT_SECRETS_FILE, SCOPES)
						
	credentials = flow.run_local_server(port=8080)
	return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def uploadVideo(title: str, pathToVid: str):
	# Create a service object
	service = get_authenticated_service()

	# Define the video metadata
	video_title = title
	video_description = ''
	video_tags = ['twitch', 'clips', 'lsf', 'forsen', 'xqc', 'dua lipa']
	video_category = '20' #gaming hopefully  # See https://developers.google.com/youtube/v3/docs/videoCategories/list
	privacy_status = 'private'

	# Define the file you want to upload
	video_file = pathToVid + title + '.mp4'

	# Create a request to upload the video
	request = service.videos().insert(
		part='snippet,status',
		body={
			'snippet': {
				'title': video_title,
				'description': video_description,
				'tags': video_tags,
				'categoryId': video_category
			},
			'status': {
				'privacyStatus': privacy_status
			}
		},
		media_body = video_file
	)

	# Execute the request and print the response
	try:
		response = request.execute()
		print(response)
	except HttpError as error:
		print(f'An error occurred: {error}')

def uploadVidList(mp4List: list, pathToVidsDir: str):
	"""
	loop through list of videos and uploads them
	"""
	for mp4 in mp4List:
		title = mp4[1]
		uploadVideo(title, pathToVidsDir)
		time.sleep(300)



# vidlist = [('https://clips-media-assets2.twitch.tv/qCkdBQBUzbWPapaEh0575w/AT-cm%7CqCkdBQBUzbWPapaEh0575w.mp4', '8th grade social studies PagMan'), ('https://clips-media-assets2.twitch.tv/J-bI1F7QPez8Lu9A0gVxxw/AT-cm%7CJ-bI1F7QPez8Lu9A0gVxxw.mp4', 'Crowding')]

# uploadVidList(vidlist, '/Users/rellamas/Downloads/2022-12-24-07-08/')
