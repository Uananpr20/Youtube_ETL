import requests
import json
from datetime import date

import os
from dotenv import load_dotenv


load_dotenv(dotenv_path = "./.env")



API_KEY = os.getenv("API_KEY")


channel_handle = "MrBeast"
maxResults = 50 

def get_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=ContentDetails&forHandle={channel_handle}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

       
        channel_items=data["items"][0]
        channel_playlistID=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistID)
        return channel_playlistID

    except requests.exceptions.RequestException as e:
        raise e
    




def get_video_ids(playlist_id):

    video_ids = []
    pageToken = None
    base_url = f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"

    try:
         
         while True:
              
              url = base_url

              if pageToken:
                   url+=f"&pageToken={pageToken}"

              response = requests.get(url)
              response.raise_for_status()
              data = response.json()
            

              for item in data.get('items',[]):
                   video_id = item['contentDetails']['videoId']
                   video_ids.append(video_id)

              pageToken = data.get('nextPageToken')

              if not pageToken:
                 break
              

         return video_ids

    except requests.exceptions.RequestException as e:
         raise e




def extract_video_data(video_ids):
     extracted_data = []

     def batch_list(video_id_list, batch_size): # video_id list is the list of video_ids and batch_size is the maxResult = 50
          for video_id in range(0, len(video_id_list),batch_size): # length would be the total size of the video (820), batch size is 50
           yield video_id_list [video_id: video_id + batch_size] # yield is use to slice the batch and send them in iteration

     try:
         
         for batch in batch_list(video_ids, maxResults): # the batch_list function gets called here using the parameters video_ids(received from the previous function)& constant assigned above for maxResults.
             video_ids_str = ",".join(batch)

             url = f"https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}"

             response = requests.get(url)
             response.raise_for_status()
             data = response.json()


             for item in data.get('items',[]):
                 video_id = item['id']
                 snippet = item['snippet']
                 statistics = item['statistics']
                 contentDetails = item['contentDetails']

                 video_data = {
                         "videoo_id" : video_id,
                         "title":snippet['title'],
                         "publishedAt":snippet['publishedAt'],
                         "duration":contentDetails['duration'],
                         "viewCount":statistics.get('viewCount',None),
                         "likeCount":statistics.get('likeCount',None),
                         "commentCount":statistics.get('commentCount', None)

                    }

                 extracted_data.append(video_data)

         return extracted_data


     except requests.exception.RequestException as e:
         raise e
     


def save_to_json(extract_data):
    file_path = f"./data/YT_ETL_data_{date.today()}.json"

    with open(file_path,"w",encoding="utf-8") as json_outputfile:
        json.dump(extract_data,json_outputfile,indent=4,ensure_ascii=False)

if __name__  == "__main__":
       playlist_id = get_playlist_id()

       video_ids= get_video_ids(playlist_id)

       video_data =extract_video_data(video_ids)

       save_to_json(video_data)
        

