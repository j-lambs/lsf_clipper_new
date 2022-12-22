import requests
import re

# gets a list of strings of the twitch clips
def getListOfClips(page_html):
	clips_list = re.findall('data-url=\"(.*?)\"', page_html)
	#REMOVE NON TWITCH LINKS FROM LIST
	twitch_only_list = []
	for x in clips_list:
		if "clips.twitch.tv" in x:
			twitch_only_list.append(x)
	return twitch_only_list

# reddit api info
CLIENT_ID = "***REMOVED***"
SECRET_KEY = "***REMOVED***"
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
data = {
	"grant_type" : "password",
	"username" : "***REMOVED***",
	"password" : "***REMOVED***"
}
#GETS REDDIT JSON TEXT
headers = {"User-Agent" : "***REMOVED***"}
res = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
TOKEN = res.json()["access_token"]
headers["Authorization"] = f"bearer{TOKEN}"
res = requests.get("https://oauth.reddit.com/r/livestreamfail/hot/", headers=headers, params={'limit' : '100'})
lsf_page_html = res.text 

# main function
print(getListOfClips(lsf_page_html))