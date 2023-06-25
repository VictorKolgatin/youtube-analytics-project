import os

from googleapiclient.discovery import build

API_KEY = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)


class Video:

    def __init__(self, id_video):
        self.id_video = id_video
        self.data = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                          id=self.id_video).execute()
        try:
            self.title = self.data['items'][0]['snippet']['title']
            self.url = f'https://www.youtube.com/watch?v={self.id_video}'
            self.viewers = self.data['items'][0]['statistics']['viewCount']
            self.likes = int(self.data['items'][0]['statistics']['likeCount'])
        except IndexError:
            self.title = None
            self.url = None
            self.viewers = None
            self.like_count = self.likes = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_video = id_video
        self.id_playlist = id_playlist

        self.data_video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                id=self.id_video).execute()

        self.data_playList = youtube.playlistItems().list(playlistId=self.id_playlist,
                                                          part='contentDetails',
                                                          maxResults=50,
                                                          ).execute()
        self.title = self.data_video['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/watch?v={self.id_video}'
        self.viewers = self.data_video['items'][0]['statistics']['viewCount']
        self.likes = int(self.data_video['items'][0]['statistics']['likeCount'])

    def __str__(self):
        return self.title
