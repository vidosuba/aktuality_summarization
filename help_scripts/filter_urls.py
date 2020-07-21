#!/usr/bin/env python3	

in_path = 'urls.txt'
out_path = 'filtered_urls.txt'
wayback_machine = 'http://web.archive.org/web/'

#http://web.archive.org/web/20140831062402id_/http://www.aktuality.sk:80/clanok/100051/oravska-poruba-za-satelit-platia-rocne-len-400-sk/

def parse_line(line):
	splitted = line.split(' ')
	parsed = {}
	if len(splitted) > 6:
		parsed = {'timestamp':splitted[1],
					'article_url':clean_article_url(splitted[2]),
					'status':splitted[4],
					'length':splitted[5] }
	return parsed

def clean_article_url(article_url):
	if article_url[-1] == '?':
		article_url = article_url[:-1]
	if article_url[-1] != '/':
		article_url = article_url + '/'
	return article_url

def get_article_number(article_url):
	parsed = article_url.split('/')
	return parsed[4]
	
def check_url(url):
	if len(url) != 4:
		return False
	if url['status'] != '200':
		return False
	return True
	
def filter_urls(urls):
	filtered_urls = []
	article_url_numbers = set()
	for line in urls.split('\n'):
		parsed = parse_line(line)
		if check_url(parsed) and get_article_number(parsed['article_url']) not in article_url_numbers:
			filtered_urls.append(parsed)
			article_url_numbers.add(get_article_number(parsed['article_url']))
	
	return filtered_urls
	
def main():

	with open(in_path,'r') as in_f:
		urls = in_f.read()

	filtered_urls = filter_urls(urls)

	with open(out_path,'w') as out_f:
		for url in filtered_urls:
			wayback_url = '{}{}id_/{}'.format(wayback_machine, url['timestamp'], url['article_url'])
			print(wayback_url, file=out_f)
		
main()


