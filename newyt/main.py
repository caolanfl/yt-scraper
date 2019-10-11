import requests, json, ChannelFinder, re, threading, time, queue
from ChannelFinder import *
from bs4 import BeautifulSoup

def find_channels(keyword):
    crawler = ChannelFinder()
    return crawler.crawl(depth, keyword)

f = open('second_kws.txt', 'r')
second_kws = f.readlines()
f.close()

i = 0
depth = int(input('Depth : '))
keyword = input('Keyword : ')
videos = find_channels(keyword)

emails = []
channels = []
que = queue.Queue()

def scrape(video_url):
    r = requests.get(url=video_url)
    channel_url = re.findall('http://www.youtube.com/channel/[A-Za-z0-9-_]+', r.content.decode('utf-8'))
    if not channel_url:
        channel_url = re.findall('http://www.youtube.com/user/[A-Za-z0-9-_]+', r.content.decode('utf-8'))
    if channel_url:
        channel_url = channel_url[0]
        channels.append(channel_url[0])

        r = requests.get(url=channel_url+'/about')
        newemails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.content.decode('utf-8'))
        if newemails:
            if [channel_url, newemails[0]] not in emails:
                return([channel_url, newemails[0]])
    else:
        print('channel not found : ', video_url)
        return 0

print('here')

i = 0
threads = []
while True:
    threads = [t for t in threads if t.is_alive()]

    if len(threads) < 500 and i<len(videos):
        URL = 'https://youtube.com'+videos[i]
        if i%20 == 0:
            print(i, len(videos))
        #thread = threading.Thread(target=scrape, args=(URL,))
        thread = threading.Thread(target=lambda q, arg1: q.put(scrape(arg1)), args=(que, URL,))
        #t = Thread(target=lambda q, arg1: q.put(foo(arg1)), args=(que, 'world!'))
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

seen = []
text_file = open(keyword+".txt", "w")
while not que.empty():
    email = que.get()
    if email != 0 and email not in seen:
        try:
            seen.append(email)
            text_file.write(email[0]+';'+email[1]+'\n')
        except:
            pass
text_file.close()

text_file = open("channels.txt", "w")
for channel in channels:
    text_file.write(channel+'\n')
text_file.close()
