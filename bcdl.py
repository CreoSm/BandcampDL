import sys
import requests
import re

def PrintUsage():
    print("""
    usage:\n
    bcdl.py [bandcamp url]\n
    \n
    Also supports multiple urls!!!\n
        bcdl.py [bandcamp url 1] [bandcamp url 2]""")

def DL(url):
    SongName = url.split("/")[4]
    print(f"Beginning Download For {SongName}")
    print("(1/3) Getting Page Data")
    r = requests.get(url, allow_redirects=True)
    content = r.text
    print("(2/3) Getting Stream Url")
    start_of_stream_url = content.find("https://t4.bcbits.com/stream")
    content = content[start_of_stream_url:]
    DownloadURL = content[:content.find("&quot")]
    print("(3/3) Downloading")
    dl = requests.get(DownloadURL, allow_redirects=True)
    open(SongName+".mp3", 'wb').write(dl.content)

def CheckURLType(url):
    if url.split("/")[3] == "track":
        DL(url)
    elif url.split("/")[3] == "album":
        print("Downloading Album")
        print("Getting Page Contents")
        r = requests.get(url, allow_redirects=True)
        content = r.text
        print("Finding Tracks")
        tracks = re.findall("&quot;/track/([A-Za-z0-9]+(-[A-Za-z0-9]+)+)&quot;,", content)
        url_thing = url.rfind("/")
        nw = url[:url_thing-1]
        url_thing = nw.rfind("/")
        nw = nw[:url_thing]
        nw = nw[:url.rfind("/")]+"/track/"
        i=1
        for track in tracks:
            print(f"DOWNLOADING -- [{i}/{len(tracks)}]")
            DL(nw+track[0])
            i+=1

if len(sys.argv) == 1:
    PrintUsage()
else:
    for v in sys.argv[1:]:
        CheckURLType(v)