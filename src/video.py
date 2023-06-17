import os

from googleapiclient.discovery import build


class Video:

    def __init__(self, id_video):
        self.id_video = id_video

        self.API_KEY = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.data = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.id_video).execute()

        self.title = self.data['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id_video}'
        self.viewers = self.data['items'][0]['statistics']['viewCount']
        self.likes = int(self.data['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.title


class PLVideo:
    def __init__(self, id_video, id_playlist):
        self.id_video = id_video
        self.id_playlist = id_playlist

        self.API_KEY = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.data_video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                 id=self.id_video).execute()

        self.data_playList = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                         part='contentDetails',
                                                         maxResults=50,
                                                         ).execute()
        self.title = self.data_video['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id_video}'
        self.viewers = self.data_video['items'][0]['statistics']['viewCount']
        self.likes = int(self.data_video['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.title
