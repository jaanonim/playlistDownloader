import concurrent.futures
import os
import string

import youtube_dl
from progress.bar import IncrementalBar
from youtubesearchpython import *

from utilities import *


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

    def get_file(self, title):
        for f in os.listdir("download"):
            if f.startswith(title) and f.endswith(".mp3"):
                return "download/" + f
        return None

    def add_to_queue(self, id, title):
        self.queue.append((id, title))

    def loop(self):
        q_len = len(self.queue)

        th_amount = calculate_amount_of_threads(q_len)

        print(f"Will donwload {q_len} videos with {th_amount} threads.")
        bar = IncrementalBar("Downloading videos ", max=q_len)

        arrays = split_list(self.queue, th_amount)

        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREDS) as executor:
            results = []
            for a in arrays:
                results.append(executor.submit(self.downloadVideos, a, bar))
            for r in results:
                r.result()

        print("")

    def downloadVideos(self, queue, bar):
        for element in queue:
            bar.next()

            id, title = element

            ydl_opts = {
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "outtmpl": f"download/{title}.mp3",
                "logger": MyLogger(),
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([f"https://www.youtube.com/watch?v={id}"])
                except:
                    pass
            # print(url)
            # r = requests.get(url, allow_redirects=True)
            # print(r)      # open(f"download/{title}.webm", "wb").write(r.content)

    def format_title(self, title):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return "".join(c for c in title if c in valid_chars)


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print("ERROR:", msg)
