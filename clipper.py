import time
start_time = time.time()

import requests
import re

from selenium import webdriver

# reddit api info
CLIENT_ID = "***REMOVED***"
SECRET_KEY = "***REMOVED***"
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
	"grant_type" : "password",
	"username" : "***REMOVED***",
	"password" : "***REMOVED***"
}

# gets a list of strings of the twitch clips
def getListOfClips(page_html):
	clips_list = re.findall('data-url=\"(.*?)\"', page_html)
	#REMOVE NON TWITCH LINKS FROM LIST
	twitch_only_list = []
	for x in clips_list:
		if "clips.twitch.tv" in x:
			twitch_only_list.append(x)
	return twitch_only_list


#GETS REDDIT JSON TEXT
def getRedditJSONText():
    headers = {"User-Agent" : "***REMOVED***"}
    res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    TOKEN = res.json()["access_token"]
    headers["Authorization"] = f"bearer{TOKEN}"
    res = requests.get("https://www.reddit.com/r/LivestreamFail/top/?sort=top&t=day", headers=headers, params={'limit' : '100'})
    return res.text

# checks if clip is missing or not
# true = clip still public
# false = clip deleted or taken down 
def checkClipValidity(url):
	# makes selenium 'headless' (NO UI)
	options = webdriver.FirefoxOptions()
	options.headless = True
	# opens new selenium window
	driver = webdriver.Firefox(options=options)
	driver.get(url=url)

	time.sleep(1) # need to wait to see if change to clip_missing page

	current_url = driver.current_url
	driver.close() # close selenium window
	if current_url == url:
		return True
	return False
	
# main function
# print(getListOfClips(getRedditJSONText()))

print(checkClipValidity("https://clips.twitch.tv/GrossWonderfulElephantDuDudu"))
print(checkClipValidity("https://clips.twitch.tv/GoldenVastLardMrDestructoid-ZI9pmwNIxd2bs6qU"))

# execution timer
print("Process finished --- %s seconds ---" % (time.time() - start_time))
