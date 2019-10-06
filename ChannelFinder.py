import time, random, csv, re, requests
from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

class ChannelFinder():

    def __init__(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        #chrome_options.add_argument('--proxy-server=%s' % '192.161.166.122:3128')
        chrome_options.add_argument("--window-size=1920x1080")

        path_to_chromedriver = 'chromedriver'
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=path_to_chromedriver)

    def crawl(self, depth, keyword):

        with open(r'youtube.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['keyword', 'user/channel'])

        playlists = []
        keyword = keyword.strip()
        print("keyword [{}]".format(keyword))
        driver = self.driver
        driver.get('https://www.youtube.com/results?search_query={}'.format(keyword))

        # Searching for only playlists
        filter_btn = driver.find_elements_by_xpath(".//paper-button[contains(@aria-label, 'Search filters')]")[0]
        filter_btn.click()
        time.sleep(1)
        playlist_btn = driver.find_elements_by_xpath(".//div[contains(@title, 'Search for Playlist')]")[0]
        playlist_btn = playlist_btn.find_element_by_xpath('..')
        playlist_btn.click()
        time.sleep(1)
        
        for i in range(depth):
            print(i)
            html = driver.find_element_by_tag_name('html')
            html.send_keys(Keys.PAGE_DOWN)
            html.send_keys(Keys.PAGE_DOWN)
            time.sleep(random.uniform(0.05, 0.1))

        response = Selector(text=str(driver.page_source))
        for r in response.xpath("//*[contains(@class, 'ytd-item-section-renderer')]"):
            try:
                playlist_url = 'https://www.youtube.com'+r.xpath(".//a[contains(@href, '/watch?v=')]/@href").extract_first()
                print(playlist_url)

                if playlist_url not in playlists:
                    playlists.append(playlist_url)
            except:
                print('gay')
        driver.quit()
        
        # getting all videos from playlists
        videos = []

        ind = 0
        for playlist in playlists:
            ind += 1
            print(ind,len(playlists))
            r = requests.get(url=playlist)
            videos += re.findall('/watch\?v=+[a-zA-Z-_.]{11}', r.content.decode('utf-8'))

        return videos
