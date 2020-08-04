#!/usr/bin/env python3	

from bs4 import BeautifulSoup, NavigableString
from blingfire import *
from os import listdir


datasets = ['training', 'test', 'validation']

def getHTMLPath(dataset, file=''):
	return f"./data/{dataset}/{file}"

def getCleanedPath(dataset, file=''):
	return f"./data/{dataset}_cleaned/{file}"

def getSumsPath(dataset, file=''):
	return f"./data/{dataset}_summs/{file}"



def getTextsFromHTML_1(html_doc):
	'''Articles where is introtext and fulltext div'''

	soup = BeautifulSoup(html_doc, 'html.parser')

	headline = soup.find('h1')
	intro = soup.find('div', class_='introtext')
	article = soup.find('div', class_='fulltext')

	if None in [headline, intro, article]:
		return None

	video = article.find('div', class_='video-ad-player-wrapper')
	if video is not None:
		article.find('div', class_='video-ad-player-wrapper').decompose()

	return headline.text, intro.text, article.text


def getTextsFromHTML_2(html_doc):
	'''Articles where is perex and fulltext div'''

	soup = BeautifulSoup(html_doc, 'html.parser')

	headline = soup.find('h1')
	intro = soup.find('div', class_='perex')
	article = soup.find('div', class_='fulltext')

	if None in [headline, intro, article]:
		return None

	video = article.find('div', class_='video-ad-player-wrapper')
	if video is not None:
		article.find('div', class_='video-ad-player-wrapper').decompose()

	return headline.text, intro.text, article.text


def getTextsFromHTML_3(html_doc):
	'''Articles where is div "obsah" and "leadArticle"'''

	soup = BeautifulSoup(html_doc, 'html.parser')

	headline = soup.find('h1')

	if headline is None:
		return None
	headline_text = headline.text



	obsah_div = soup.find('div', class_='obsah')
	leadArticle_p = soup.find('p', class_='leadArticle')
	zdroj_p = soup.find('p', class_='zdroj')

	if None in [obsah_div, leadArticle_p, zdroj_p]:
		return None

	obsah_text = obsah_div.text
	leadArticle_text = leadArticle_p.text
	zdroj_text = zdroj_p.text

	ix_lead = obsah_text.find(leadArticle_text)

	if ix_lead == -1:
		return None

	intro_text = obsah_text[:ix_lead]
	intro_text = intro_text.replace(headline_text, '')
	article_text = obsah_text[ix_lead + len(leadArticle_text):]
	article_text = article_text.replace(zdroj_text, '')

	if '' in [headline_text, article_text]:
		return None

	return headline_text.strip(), intro_text.strip(), article_text.strip()


def tokenize(text):
	return text_to_words(text)

def getUncleaned(dataset):
	all_files = set(listdir(getHTMLPath(dataset)))
	cleaned = set(listdir(getCleanedPath(dataset)))
	return all_files - cleaned


def parse_dataset(dataset):
	'''Parse html files and get headlines, intro(abstract) and article body. Saves to new location.
	   Function getTextsFromHTML_x does parsing, each for different html structure.'''

	files = getUncleaned(dataset)
	print(f"PARSING {dataset}, length:{len(files)}")

	good_count = 0
	for c, f in enumerate(files):

		with open(getHTMLPath(dataset, f), 'r') as r:
			html_doc = r.read()
		text = getTextsFromHTML_3(html_doc)
		if text is not None:
			headline, intro, article = text
			with open(getCleanedPath(dataset, f), 'w') as out_f:
				print('{}\n{}\n{}\n'.format(tokenize(headline), tokenize(intro), tokenize(article)), file=out_f)
			good_count += 1

		if c % 1000 == 0:
			print(f"{c}/{len(files)}, good:{good_count}")


def make_summs(dataset):
	'''Make summarization from headline and abstract. Also it is needed because before 
	   I forgot to strip article parts.'''

	files = set(listdir(getCleanedPath(dataset)))
	print(f"MAKING SUMMS {dataset}, length:{len(files)}")

	for c, f in enumerate(files):
		with open(getCleanedPath(dataset, f), 'r') as in_f:
			content = in_f.read()

		content = content.split('\n')
		content = list(filter(lambda x: len(x) != 0, content))
		if len(content) == 2:
			headline, article = content
			intro = ''
		elif len(content) == 3:
			headline, intro, article = content
		else:
			continue

		intro = intro.replace('ilustračné foto', '')
		sum_ = f"{headline} {intro}"

		with open(getSumsPath(dataset, f), 'w') as out_f:
			print('{}\n{}'.format(sum_, article), file=out_f)

		if c % 1000 == 0:
			print(f"{c}/{len(files)}")



def main():
	
	# for dataset in datasets:
	# 	parse_dataset(dataset)

	for dataset in datasets:
		make_summs(dataset)


main()
