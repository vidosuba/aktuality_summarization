with open('urls.txt','r') as in_f:
	with open('urls_short.txt','w') as out_f:
		urls = in_f.read()
		short_urls = urls[:10000]
		print(short_urls, file=out_f)

