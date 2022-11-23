def fuc(method,URL):
	if method == 1:
		"""only works for playlist which have less then 100 videos"""
		import requests
		import re

		page = requests.get(URL)

		pattern = "\\{\"accessibility\":\\{\"accessibilityData\":\\{[^}]*\\}\\},\"simpleText\":\"[^\"]*\"\\}"
		dl = list(set(re.findall(pattern, page.text)))
		pa1 = "\\d*:\\d*:\\d*"
		pa2 = '"."\\d*:\\d*"'
		durations = []
		for i in dl:
			pal1 = re.findall(pa1, i)
			if len(pal1) != 0:
				durations.append(pal1[0][:])
		for i in dl:
			pal2 = re.findall(pa2, i)
			if len(pal2) != 0:
				durations.append(pal2[0][3:-1])
		# print(len(durations),sorted(durations))

		def sol2(arr): 
			days = hours = mins = secs = 0  
			for duration in arr: 
				try:  
					secs += int(duration[-2:])  
					mins += int(duration[-5:-3])  
					hours += int(duration[:-6])  
				except ValueError:  
					continue  
			mins += (secs//60)  
			secs %= 60  
			hours += (mins//60)  
			mins %= 60  
			days = hours//24  
			hours %= 24  
			return (f'{days}day,' if days > 0 else '') + (f'{hours}Hr,' if hours > 0 else '') + (f'{mins}min,' if mins > 0 else '') + (f'{secs}sec')
		 
		print(sol2(durations))
		return sol2(durations)

	elif method == 2:
		from selenium import webdriver
		from selenium.webdriver.common.by import By
		from selenium.webdriver.common.keys import Keys
		from selenium.webdriver.chrome.service import Service
		from bs4 import BeautifulSoup as soup
		import re

		def get_html():
			innerHTML = driver.execute_script("return document.body.innerHTML")
			page_soup = soup(innerHTML, 'html.parser')
			return page_soup

		chrome_options = webdriver.ChromeOptions()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument("--incognito")

		ser = Service("G:\\My Drive\\projects\\Scrappers\\Brave Scrapper\\chromedriver.exe")
		driver = webdriver.Chrome(service=ser,options=chrome_options)
		driver.get(URL)
		pat1 = r'"numVideosText":\{"runs":\[\{"text":"([,0-9]*)"\},\{"text":" videos"\}]\}'
		ns = re.findall(pat1, driver.execute_script("return document.body.innerHTML"))
		times_scroll_down = int((int(ns[0].replace(",",""))/100) + 2)
		for i in range(times_scroll_down):
			elm = driver.find_element(By.TAG_NAME,'html')
			elm.send_keys(Keys.END)
			import time
			time.sleep(1)
		page_soup = get_html()
		driver.quit() # stop the driver
		tc = page_soup.findAll('span', {'class':'style-scope ytd-thumbnail-overlay-time-status-renderer'})
		pat2 = r'\n  ([0-9]+(:[0-9]+)+)\n'
		lt = [re.findall(pat2, str(i))[0][0] for i in tc]
		# print(int(ns[0]),len(lt),lt)

		def sol2(arr): 
			days = hours = mins = secs = 0  
			for duration in arr: 
				try:  
					secs += int(duration[-2:])  
					mins += int(duration[-5:-3])  
					hours += int(duration[:-6])  
				except ValueError:  
					continue  
			mins += (secs//60)  
			secs %= 60  
			hours += (mins//60)  
			mins %= 60  
			days = hours//24  
			hours %= 24  
			return (f'{days}day,' if days > 0 else '') + (f'{hours}Hr,' if hours > 0 else '') + (f'{mins}min,' if mins > 0 else '') + (f'{secs}sec')
		 
		print(sol2(lt))
		return sol2(lt)

	elif method == 3:
		# 1. Create a [YouTube Data v3 API key](https://developers.google.com/youtube/registering_an_application)
		# 2. Replace the strings with your own API key and playlist ID.

		from datetime import timedelta
		import datetime
		import isodate
		import json
		import requests
		import re

		def duration_format(a):
			pattern = '(([0-9]+) day[s]?, )?([0-9]+):([0-9]+):([0-9]+)'
			ree = re.findall(pattern, str(a))

			if ree[0][-4] != '':
				days = int(ree[0][-4])
			else : days = 0

			hours = int(ree[0][-3])
			mins = int(ree[0][-2])
			secs = int(ree[0][-1])

			return (f'{days}day, ' if days > 0 else '') + (f'{hours}hr, ' if hours > 0 else '') + (f'{mins}min, ' if mins > 0 else '') + (f'{secs}sec ')

		# replace with your api
		yt_api = 'AIzaSyDnSqPzpYdW39YctSY8YofjMkcHDXc0yWM' 
		# replace with your playlist_id
		playlist_id = URL[URL.index("=")+1:]

		URL1 = 'https://www.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults=50&fields=items/contentDetails/videoId,nextPageToken&key={}&playlistId={}&pageToken='.format(yt_api, playlist_id)
		URL2 = 'https://www.googleapis.com/youtube/v3/videos?&part=contentDetails&key={}&id={}&fields=items/contentDetails/duration'.format(yt_api, "{}")

		next_page = ''
		cnt = 0
		a = timedelta(0)

		while True:

			vid_list = []

			results = json.loads(requests.get(URL1 + next_page).text)

			for x in results['items']:
				vid_list.append(x['contentDetails']['videoId'])
				
			cnt += len(vid_list)

			url_list = ','.join(vid_list)

			op = json.loads(requests.get(URL2.format(url_list)).text)

			for x in op['items']:
				a += isodate.parse_duration(x['contentDetails']['duration'])

			if 'nextPageToken' in results:
				next_page = results['nextPageToken']
			else:
				print(f'Total length of playlist : {str(a)} : {duration_format(a)}',
						f'\nNo of videos : {str(cnt)} : {int(cnt)}', 
						f'\nAverage length of video : {str(a/cnt)} : {duration_format(a/cnt)}',
						f'\nAt 1.25x : {str(a/1.25)} : {duration_format(a/1.25)}', 
						f'\nAt 1.50x : {str(a/1.5)} : {duration_format(a/1.5)}', 
						f'\nAt 1.75x : {str(a/1.75)} : {duration_format(a/1.75)}', 
						f'\nAt 2.00x : {str(a/2)} : {duration_format(a/2)}')
				return duration_format(a)
				break

def arg_check(method,URL):
	if method!=1 and method!=2 and method!=3 : print("Choose method from 1 2 3 only");quit()
	if URL == "" : print("Enter URL");quit()
