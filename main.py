import concurrent.futures

from progress.bar import IncrementalBar
from youtubesearchpython import Playlist

from music_downloader import MusicDownloader
from utilities import *


def add_to_queue(id, title, fetcher):
    if not MusicDownloader.getInstance().get_file(title):
        MusicDownloader.getInstance().add_to_queue(id, title, fetcher)
        return False
    return True


def playlist(url):
    print("Getting videos ...")
    playlist = Playlist(url)

    while playlist.hasMoreVideos:
        playlist.getNextVideos()

    videos = playlist.videos
    v_len = len(videos)

    print(f"Found {v_len} videos.")

    th_amount = calculate_amount_of_threads(v_len)
    print(f"Loading videos with {th_amount} threads ...")
    bar = IncrementalBar("", max=v_len)

    arrays = split_list(videos, th_amount)

    suma = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREDS) as executor:
        results = []
        for a in arrays:
            results.append(executor.submit(analizeVideos, a, bar))
        for r in results:
            suma += r.result()

    print("")
    print(f"The average song length in this playlist is: {suma/v_len}s")


def analizeVideos(videos, bar):
    fetcher = MusicDownloader.getInstance().get_fetcher()
    suma = 0
    for v in videos:
        bar.next()
        add_to_queue(
            v["id"], MusicDownloader.getInstance().format_title(v["title"]), fetcher
        )

        m, s = v["duration"].split(":")
        suma += int(m) * 60 + int(s)
    return suma


def main():
    # url = input("Enter playlist url: ")
    url = "https://www.youtube.com/playlist?list=PLWY-qomjS4TN6Ejw3_aleGjynl_ZUwPtk"
    playlist(url)
    MusicDownloader.getInstance().loop()
    print("Done!")


if __name__ == "__main__":
    main()
