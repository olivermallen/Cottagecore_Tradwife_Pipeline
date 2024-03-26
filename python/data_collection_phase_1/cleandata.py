import pickle
import pandas as pd
import requests
import shutil 
import os
import sys
from bs4 import BeautifulSoup

#first work without images? just takes a long time to download and a lot of space, maybe get a separate drive

def fetch_image(url, filename):
    """
    fetches image at url and saves it with filename
    """
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True
            # Open a local file with wb ( write binary ) permission.
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)
    except:
        print("unable to download image")


def addpost(post, dataframedict):
    "function to add post to dataframedict"
    #time posted
    dataframedict['time_posted'].append(post['date'])
    #blog name
    dataframedict['blog_name'].append(post['blog_name'])
    #post id
    dataframedict['post_id'].append(post['id_string'])
    #post type
    dataframedict['post_type'].append(post['type'])
    #image_urls
    #first I need to extract all image urls from json object which are in post['body'] and post['reblog']['comment'] OR post['photos'] photo['original_size']['url']
    image_urls = []
    if 'body' in post:
        soup = BeautifulSoup(post['body'])
        images = soup.find_all('img')
        for image in images:
            image_urls.append(image.get("src"))
    elif 'photos' in post:
        for photo in post['photos']:
            soup = BeautifulSoup(photo['original_size']['url'])
            images = soup.find_all('img')
            for image in images:
                image_urls.append(image.get("src"))
    if 'reblog' in post:
        soup = BeautifulSoup(post['reblog']['comment'])
        images = soup.find_all('img')
        for image in images:
            image_urls.append(image.get("src"))
    dataframedict['image_urls'].append(image_urls)
    #now download images
    # i = 0
    # for image in image_urls:
    #     fetch_image(image, "images/"+post["id_string"]+"_"+str(i)+".jpg")
    #     i = i + 1
    #tags
    dataframedict["tags"].append(post["tags"])
    #post text
    # if post["type"]=="photo":
    #     raw_text = post["caption"]
    # elif post["type"]=="quote":
    #     raw_text = post["text"]
    # else:
    #     try:
    #         raw_text = post["body"]
    #     except KeyError:
    #         raw_text = ""
    # dataframedict["post_text"].append(raw_text)
    #post url
    dataframedict["post_url"].append(post["post_url"])

dictionary = {'time_posted':[], 'blog_name':[], 'post_id':[], 'post_type':[], 'image_urls':[], 'tags':[], 'post_url':[]}

#import posts 
i = 0
pickle_directories = sys.argv[1:] 
for folder in pickle_directories:
    picklefiles = os.listdir(folder)
    for file in picklefiles:
        with open(folder+"/"+file, 'rb') as f:
            posts = pickle.load(f)
            for post in posts:
                addpost(post, dictionary)
        i = i+1
        if i%100==0:
            print("working on file "+str(i))

print("saving to pickle file...")
df = pd.DataFrame.from_dict(dictionary)
df.to_pickle("full_data.pkl", compression='infer', protocol=5, storage_options=None)