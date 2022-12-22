import time
start_time = time.time()

import requests
import re
import urllib.request

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
 

# main function
# print(getListOfClips(getRedditJSONText()))
request = urllib.request.urlopen(url="https://clips.twitch.tv/GrossWonderfulElephantDuDudu",timeout=3)
# resp = urllib.request.urlopen(request, timeout=3)
print(request.geturl())

print("Process finished --- %s seconds ---" % (time.time() - start_time))
