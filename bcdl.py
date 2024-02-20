import sys
import requests

def PrintUsage():
    print("bcdl.py [bandcamp url]")
    print("Also supports multiple urls!!!")
    print("bcdl.py [bandcamp url 1] [bandcamp url 2]")

Allow=False # To skip first argv parameter

def DL(url):
    print("(1/3) Getting Page Data")
    r = requests.get(url, allow_redirects=True)
    content = r.text
    print("(2/3) Getting Stream Url")
    start_of_stream_url = content.find("https://t4.bcbits.com/stream")
    content = content[start_of_stream_url:]
    DownloadURL = content[:content.find("&quot")]
    print("(3/3) Downloading")
    dl = requests.get(DownloadURL, allow_redirects=True)
    open(DownloadURL.split("/")[4]+".mp3", 'wb').write(dl.content)
if len(sys.argv) == 0:
    PrintUsage()
else:
    for v in sys.argv:
        if Allow:
            print(f"Downloading {v}")
            DL(v)
        else:
            Allow=True
