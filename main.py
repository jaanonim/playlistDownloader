from progress.bar import IncrementalBar
from youtubesearchpython import Playlist

from music_downloader import MusicDownloader


def add_to_queue(id, title):
    if not MusicDownloader.getInstance().get_file(title):
        MusicDownloader.getInstance().add_to_queue(id, title)
        return False
    return True


def playlist(url):
    print("Getting videos ...")
    playlist = Playlist(url)

    while playlist.hasMoreVideos:
        playlist.getNextVideos()

    videos = playlist.videos

    print(f"Found {len(videos)} videos.")

    bar = IncrementalBar("Loading videos ", max=len(videos))

    suma = 0
    for v in videos:
        bar.next()
        add_to_queue(v["id"], MusicDownloader.getInstance().format_title(v["title"]))

        m, s = v["duration"].split(":")
        suma += int(m) * 60 + int(s)

    print("")
    print(f"The average song length in this playlist is: {suma/len(videos)}s")


def main():
    url = input("Enter playlist url: ")
    playlist(url)
    MusicDownloader.getInstance().loop()
    print("Done!")


if __name__ == "__main__":
    main()
