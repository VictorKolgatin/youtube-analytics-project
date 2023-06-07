import json
import os
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""

    youtube = None

    def __init__(self, channel_id):
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.API_KEY = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.API_KEY)
        self.__channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()

        self.title = self.channel["items"][0]["snippet"]["title"]
        self.description = self.channel["items"][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriberCount = self.channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = self.channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = self.channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.channel = json.dumps(self.channel, indent=2, ensure_ascii=False)
        print(f'{self.channel}')

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            print("False name or invalid")

    @classmethod
    def get_service(cls):
        id_channel = input("Введите id канала: ")
        youtube = build('youtube', 'v3', developerKey='AIzaSyDAKyCWtI_f-A9-ob8OYtx_YqdOVEC-gRU')
        channel = youtube.channels().list(id=id_channel, part='snippet,statistics').execute()
        youtube_channel = Channel(id_channel)
        return f'Канал: {channel}' \
               f'Создан объект класса "Channel" {youtube_channel}'


    def to_json(self, file_name=None):
        with open(file_name, 'w') as file:
            json.dump(self.channel, file)

