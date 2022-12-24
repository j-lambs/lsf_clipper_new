from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time

def get_YYYY_MM_DD_Hr_Min():
    today = time.strftime("%Y-%m-%d-%H-%M")
    return today

def genTwClipsDLLink(clip_url: str):
    """
    returns a tuple of (link to mp4, clip title)    
    """
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


def twDLLinkList(valid_links_list: list):
    """
    valid links as arg \n
    generates list of links of mp4 from valid links
    """
    mp4List = []
    for valid_link in valid_links_list:
        mp4List.append(genTwClipsDLLink(valid_link))
    return mp4List


def downloadMP4(url, title):
    """
    downloads single mp4 from web.
    downloads end in Downloads directory
    """
    file_name = title + ".mp4"
    r = requests.get(url)
    print("****Connected****")

    dateAndTime = get_YYYY_MM_DD_Hr_Min()
    os.mkdir('/Users/rellamas/Downloads/' + dateAndTime) # makes new directory
    f = open(f'/Users/rellamas/Downloads/{dateAndTime}/{file_name}', 'wb') # videos downloaded here
    print("Downloading.....")
    for chunk in r.iter_content(chunk_size=255): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    print("Done")
    f.close()


def download_list_of_MP4s(mp4List: list):
    """
    downloads a from a list of links to MP4s
    """
    [downloadMP4(clipElement[0], clipElement[1]) for clipElement in mp4List]



