import os
import string

import requests
from progress.bar import IncrementalBar
from youtubesearchpython import *


class MusicDownloader:
    __instance = None

    @staticmethod
    def getInstance():
        if MusicDownloader.__instance == None:
            MusicDownloader()
        return MusicDownloader.__instance

    def __init__(self):
        if MusicDownloader.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            MusicDownloader.__instance = self

        self.queue = []
        self.fetcher = StreamURLFetcher()

    def get_file(self, title):
        for f in os.listdir("download"):
            if f.startswith(title):
                return "download/" + f
        return None

    def add_to_queue(self, id, title):
        while not self.fetcher:
            pass
        video = Video.get(f"https://www.youtube.com/watch?v={id}")
        url = self.fetcher.get(video, 251)
        self.queue.append((url, id, title))

    def loop(self):
        print(f"Will donwload {len(self.queue)} videos.")
        bar = IncrementalBar("Loading videos ", max=len(self.queue))

        while len(self.queue) > 0:
            url, id, title = self.queue[0]
            self.queue.pop(0)

            bar.next()

            r = requests.get(url, allow_redirects=True)
            open(f"download/{title}.webm", "wb").write(r.content)
        print("")

    def format_title(self, title):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return "".join(c for c in title if c in valid_chars)
