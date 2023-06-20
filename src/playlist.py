from googleapiclient.discovery import build

from src.video import PLVideo
import datetime

import isodate


class DataPL:
    YT_API_KEY = 'AIzaSyDAKyCWtI_f-A9-ob8OYtx_YqdOVEC-gRU'
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, id_playlist):
        self.id_playlist = id_playlist

    def get_video(self):
        """
        Из плейлиста, по id, получаем данные по видеороликам
        """

        video = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                  part='contentDetails',
                                                  maxResults=50,
                                                  ).execute()
        return video

    def get_video_id(self):
        """
        Получаем все id видеороликов из плейлиста
        """

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in
                                self.get_video()['items']]
        return video_ids


class PlayList(DataPL, PLVideo):
    def __init__(self, id_playlist):
        super().__init__(id_playlist)
        self.data = self.get_data(id_playlist)
        self.title = self.data['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={id_playlist}'

    def get_data(self, id_playlist):
        """ Получаем данные от YouTube по id плейлиста. """

        self.data = self.youtube.playlists().list(part='snippet',
                                                  id=id_playlist).execute()
        return self.data

    def show_best_video(self):
        """
        Возвращаем ссылку на самое популярное видео из плейлиста (по
        количеству лайков).
        """

        best_like = {}
        for i in self.get_video_id():
            video = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=i).execute()
            like = (video['items'][0]['statistics']['likeCount'])
            best_like[i] = int(like)
            max_val_key = max(best_like, key=best_like.get)

        return f'https://youtu.be/{max_val_key}'

    @property
    def total_duration(self):
        """
        Возвращает объект класса `datetime.timedelta` с суммарной
        длительность плейлиста.(обращение как к свойству, использовать @property)
        """

        video_response = self.youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(self.get_video_id())
        ).execute()
        total_time = datetime.timedelta()

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time
