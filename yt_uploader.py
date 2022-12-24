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


def uploadVideo():
	# Create a service object
	service = get_authenticated_service()

	# Define the video metadata
	video_title = 'testing...'
	video_description = 'This is a video I uploaded with the YouTube API'
	video_tags = ['twitch', 'clips', 'lsf', 'forsen', 'xqc', 'dua lipa']
	video_category = 'Gaming'  # See https://developers.google.com/youtube/v3/docs/videoCategories/list

	# Define the file you want to upload
	video_file = '/Users/rellamas/Downloads/good one mr fors.mp4'

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
				'privacyStatus': 'private'
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
