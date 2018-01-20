from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as pd
import csv

# API KEY
DEVELOPER_KEY = "AIzaSyB8Pe7LqpwNK_AKWWgFREyMHy3UwwsgCIU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#scraper 

def youtube_search(q, max_results=50,order="relevance", token=None, location=None, location_radius=None):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    search_response = youtube.search().list(
    q=q,
    type="video",
    pageToken=token,
    order = order,
    part="id,snippet", # Part signifies the different types of data you want 
    maxResults=max_results,
    location=location,
    locationRadius=location_radius).execute()

    res = []
    for search_result in search_response.get("items", []):
       if search_result["id"]["kind"] == "youtube#video":
        row = {}
        row['title']=search_result['snippet']['title']
        row['videoId']=search_result['id']['videoId']
        response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()
        row["channelId"]= response['items'][0]['snippet']['channelId']
        row['channelTitle'] = response['items'][0]['snippet']['channelTitle']
        if 'tags' in response['items'][0]['snippet'].keys():
            row['tags'] = response['items'][0]['snippet']['tags']
        else:
            row['tags'] = 'na'
        row['categoryId'] = response['items'][0]['snippet']['categoryId']
        row['favorateCount'] = response['items'][0]['statistics']['favoriteCount']
        if 'viewCount' in response['items'][0]['statistics'].keys():
            row['viewCount'] = response['items'][0]['statistics']['viewCount']
        else:
            row['viewCount'] = 'na'
        if 'likeCount' in response['items'][0]['statistics'].keys():
            row['likeCount'] = response['items'][0]['statistics']['likeCount']
        else:
            row['likeCount'] = 'na'
        if 'likeCount' in response['items'][0]['statistics'].keys():
            row['dislikeCount'] = response['items'][0]['statistics']['dislikeCount']
        else:
            row['dislikeCount'] = 'na'   
        if 'commentCount' in response['items'][0]['statistics'].keys():
            row['commentCount'] = response['items'][0]['statistics']['commentCount']
        else:
            row['commentCount'] = 'na'
        
        res.append(row)
        
    return res

##saving data
data = [] 

with open('vblogger_namelist.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        print(row)
        videos = youtube_search(row)
        df = pd.DataFrame(videos)
        data.append(df)
 
##iterate names in list to collect data
for i in range(0,16):
    data[i].to_csv(str(i))

o = pd.read_csv("0")
o["videoId"] = "https://www.youtube.com/watch?v="+o['videoId'].astype(str)

##save them in different csv
for i in range(1,16):
    m = pd.read_csv(str(i))
    m["videoId"] = "https://www.youtube.com/watch?v="+m['videoId'].astype(str)
    o = o.append(m)
o.to_csv("youtube_hiv_data.csv",encoding="UTF-8")
# saving all in one csv

with open('vblogger_namelist.csv') as file:  
    reader = csv.reader(file)
    n = list(reader)
print (n)

##create a name list "a"
x = 0
a = n[x]
for i in range(1,17):
    a = a+n[i]
    
df=pd.read_csv("youtube_hiv_data.csv")
df = df[df.channelTitle.isin(a)]
df.to_csv("youtube_hiv_data_cleaned.csv",encoding="UTF-8")

