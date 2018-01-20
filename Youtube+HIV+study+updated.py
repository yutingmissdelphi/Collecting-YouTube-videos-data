
# coding: utf-8

# In[ ]:


from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as pd

DEVELOPER_KEY = "AIzaSyB8Pe7LqpwNK_AKWWgFREyMHy3UwwsgCIU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


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

    title = []
    channelId = []
    channelTitle = []
    categoryId = []
    videoId = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    commentCount = []
    favoriteCount = []
    category = []
    tags = []
    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":

            title.append(search_result['snippet']['title']) 

            videoId.append(search_result['id']['videoId'])

            response = youtube.videos().list(
                part='statistics, snippet',
                id=search_result['id']['videoId']).execute()

            channelId.append(response['items'][0]['snippet']['channelId'])
            channelTitle.append(response['items'][0]['snippet']['channelTitle'])
            categoryId.append(response['items'][0]['snippet']['categoryId'])
            
        if 'favoriteCount' in response['items'][0]['statistics'].keys():
            favoriteCount.append(response['items'][0]['statistics']['favoriteCount'])
        else:
            favorateCount.append([])
        
        if 'viewCount' in response['items'][0]['statistics'].keys():
            viewCount.append(response['items'][0]['statistics']['viewCount'])
        else:
            viewCount.append([])
            
    
        if 'likeCount' in response['items'][0]['statistics'].keys():
            likeCount.append(response['items'][0]['statistics']['likeCount'])
        else:
            commentCount.append([])
        if 'dislikeCount' in response['items'][0]['statistics'].keys():
            dislikeCount.append(response['items'][0]['statistics']['dislikeCount'])
        else:
            commentCount.append([])

        if 'commentCount' in response['items'][0]['statistics'].keys():
            commentCount.append(response['items'][0]['statistics']['commentCount'])
        else:
            commentCount.append([])

        if 'tags' in response['items'][0]['snippet'].keys():
            tags.append(response['items'][0]['snippet']['tags'])
        else:
            tags.append([])

    youtube_dict = {'tags':tags,'channelId': channelId,'channelTitle': channelTitle,'categoryId':categoryId,'title':title,'videoId':videoId,'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,'commentCount':commentCount,'favoriteCount':favoriteCount}

    return youtube_dict


import pandas as pd


import matplotlib.pyplot as plt

import seaborn as sns

test = youtube_search("Nakeisa Jackson")
test.keys()

df = pd.DataFrame(data=test)


df1 = df[['title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']]

df1.columns = ['Title','viewCount','channelTitle','commentCount','likeCount','dislikeCount','tags','favoriteCount','videoId','channelId','categoryId']


# In[ ]:


df1['videoId']="https://www.youtube.com/watch?v="+df1['videoId'].astype(str)


# In[ ]:


from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pandas as pd
import pprint 
import matplotlib.pyplot as pd

DEVELOPER_KEY = "AIzaSyB8Pe7LqpwNK_AKWWgFREyMHy3UwwsgCIU"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


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


# In[2]:


##video = youtube_search("Robert Williams")


# In[3]:


#import pandas as pd
#data = pd.DataFrame(video)


# In[4]:


#data


# In[5]:


import csv
import pandas as pd
data = [] 

with open('vblogger_namelist.csv', newline='') as File:  
    reader = csv.reader(File)
    for row in reader:
        print(row)
        videos = youtube_search(row)
        df = pd.DataFrame(videos)
        data.append(df)
    


# In[16]:


for i in range(0,16):
    data[i].to_csv(str(i))

o = pd.read_csv("0")
o["videoId"] = "https://www.youtube.com/watch?v="+o['videoId'].astype(str)


# In[17]:


for i in range(1,16):
    m = pd.read_csv(str(i))
    m["videoId"] = "https://www.youtube.com/watch?v="+m['videoId'].astype(str)
    o = o.append(m)


# In[18]:


len(o)


# In[19]:





o.to_csv("youtube_hiv_data.csv",encoding="UTF-8")



# In[20]:


with open('vblogger_namelist.csv') as file:  
    reader = csv.reader(file)
    n = list(reader)
print (n)


# In[21]:


##create a name list "a"
x = 0
a = n[x]
for i in range(1,17):
    a = a+n[i]


# In[22]:


df=pd.read_csv("youtube_hiv_data.csv")


# In[23]:




df = df[df.channelTitle.isin(a)]


# In[24]:


df.to_csv("youtube_hiv_data_cleaned.csv",encoding="UTF-8")



# In[25]:


len(df)

