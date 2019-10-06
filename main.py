import requests, json, re, threading, time

filename = input('Playlist list : ')
f = open(filename, 'r')
playlists = f.readlines()

videos = []
def get_videos(playlist_url):
    r = requests.get(url=playlist_url)
    for video in re.findall('/watch\?v=+[a-zA-Z-_.]{11}', r.content.decode('utf-8')):
        videos.append(video)


emails = []
def scrape(video_url):
    r = requests.get(url=video_url)
    channel_url = re.findall('http://www.youtube.com/channel/[A-Za-z0-9-_]+', r.content.decode('utf-8'))
    if not channel_url:
        channel_url = re.findall('http://www.youtube.com/user/[A-Za-z0-9-_]+', r.content.decode('utf-8'))
    if channel_url:
        channel_url = channel_url[0]

        r = requests.get(url=channel_url+'/about')
        newemails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.content.decode('utf-8'))
        if newemails:
            if [channel_url, newemails[0]] not in emails:
                emails.append([channel_url, newemails[0]])

print('here')

i = 0
threads = []
while True:
    threads = [t for t in threads if t.is_alive()]

    if len(threads) < 100 and i<len(playlists):
        URL = playlists[i]
        if i%20 == 0:
            print(i, len(playlists))
        thread = threading.Thread(target=get_videos, args=(URL,))
        threads.append(thread)
        thread.start()

        i += 1

    # Break when all threads are finished
    flag = False
    if i == len(playlists):
        flag = True
        for t in threads:
            if t.is_alive():
                flag = False
                break
    if flag:
        break

i = 0
threads = []
while True:
    threads = [t for t in threads if t.is_alive()]

    if len(threads) < 100 and i<len(videos):
        URL = 'https://youtube.com'+videos[i]
        if i%20 == 0:
            print(i, len(videos))
        thread = threading.Thread(target=scrape, args=(URL,))
        threads.append(thread)
        thread.start()

        i += 1

    # Break when all threads are finished
    flag = False
    if i == len(videos):
        flag = True
        for t in threads:
            if t.is_alive():
                flag = False
                break
    if flag:
        break

text_file = open(keyword+"fsd.txt", "w")
for email in emails:
    text_file.write(email[0]+';'+email[1]+'\n')
text_file.close()
