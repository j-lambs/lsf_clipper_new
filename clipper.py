import time
import requests
import re
import concurrent.futures
from selenium import webdriver
from dl_clips import *

# reddit api info
CLIENT_ID = "***REMOVED***"
SECRET_KEY = "***REMOVED***"
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
	"grant_type" : "password",
	"username" : "***REMOVED***",
	"password" : "***REMOVED***"
}

# returns a list of strings of the twitch clips
def getListOfClips(page_html: str):
	clips_list = re.findall('data-url=\"(.*?)\"', page_html)
	#REMOVE NON TWITCH LINKS FROM LIST
	twitch_only_list = []
	for x in clips_list:
		if "clips.twitch.tv" in x:
			twitch_only_list.append(x)
	return twitch_only_list


# RETURNS REDDIT JSON TEXT
def getRedditJSONText() -> str:
    headers = {"User-Agent" : "***REMOVED***"}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    TOKEN = res.json()["access_token"]
    headers["Authorization"] = f"bearer{TOKEN}"
    res = requests.get("https://www.reddit.com/r/LivestreamFail/top/?sort=top&t=day", headers=headers, params={'limit' : '6'}) # limit is actually limit -1
    return res.text

# checks if clip is missing or not
# true = clip still public
# false = clip deleted or taken down 
def verifyClip(url: str):
	# makes selenium 'headless' (NO UI)
	options = webdriver.FirefoxOptions()
	options.headless = True
	# opens new selenium window
	driver = webdriver.Firefox(options=options)
	driver.get(url=url)

	time.sleep(1.25) # need to wait to see if change to clip_missing page

	current_url = driver.current_url
	driver.close() # close selenium window
	if current_url == url:
		return True
	return False

# verifies clips in clip_list and appends valid clips to valid_clip_list
# returns valid_clip_list
def verifiedClipsList(clip_list: list):
	valid_clip_list = []
	for my_url in clip_list:
		if verifyClip(my_url):
			valid_clip_list.append(my_url)
	return valid_clip_list

# main function
start_time = time.time()
clip_list = getListOfClips(getRedditJSONText())

valid_clip_list = verifiedClipsList(clip_list)
print(valid_clip_list)

my_mp4_list = twDLLinkList(valid_clip_list)
print(my_mp4_list)

print("Process finished --- %s seconds ---" % (time.time() - start_time))
