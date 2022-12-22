from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

# returns a tuple of (link to mp4, clip title)
def genTwClipsDLLink(clip_url: str):
    # makes selenium 'headless' (NO UI)
    options = webdriver.FirefoxOptions()
    options.headless = True
    # opens new selenium window
    driver = webdriver.Firefox(options=options)
    driver.get(url='https://clipsey.com/')
    
    # locates searchbar
    searchbox = driver.find_element(By.CLASS_NAME, 'clip-url-input')
    # input twitch clip url into searchbar
    searchbox.send_keys(clip_url)

    # finds and clicks 'DOWNLOAD CLIP' button
    searchButton = driver.find_element(By.CLASS_NAME, 'get-download-link-button')
    searchButton.click()

    # explicit wait
    # waits for download element to be clickable
    WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CLASS_NAME, 'download-clip-link')))
    downloadButton = driver.find_element(By.CSS_SELECTOR, 'a.download-clip-link')
    mp4link = downloadButton.get_attribute('href')
    
    # get clip title
    clipTitleElement = driver.find_element(By.CLASS_NAME, 'clip-title')
    clipTitle = clipTitleElement.get_attribute('innerHTML')


    driver.quit()
    return (mp4link, clipTitle)

# print(genTwClipsDLLink('https://www.twitch.tv/ratirl/clip/HonestNiceEchidnaBleedPurple-9RuOFX2tI9lzXJ67'))

# valid links as arg
# generates list of links of mp4 from valid links
def twDLLinkList(valid_links_list: list):
    mp4List = []
    for valid_link in valid_links_list:
        mp4List.append(genTwClipsDLLink(valid_link))
    return mp4List





# downloads single mp4 from web
# downloads end in Downloads directory
def downloadFile(name, url):
    name = name + ".mp4"
    r = requests.get(url)
    print("****Connected****")
    f = open(f'/Users/rellamas/Downloads/{name}', 'wb')
    print("Donloading.....")
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print("Done")
    f.close()
# downloadFile('n1', 'https://clips-media-assets2.twitch.tv/9GYxs7N-b1oFGq5G0kolbA/AT-cm%7C9GYxs7N-b1oFGq5G0kolbA.mp4')
