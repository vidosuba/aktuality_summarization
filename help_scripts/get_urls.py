#!/usr/bin/env python3	

import requests 
  
# Making a get request 
url = 'http://web.archive.org/cdx/search/cdx?url=aktuality.sk/clanok/*&output=txt'
response = requests.get(url) 
  
# saving request 
with open('urls.txt','w') as f:
	print(response.text, file=f) 
