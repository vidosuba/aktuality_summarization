#!/usr/bin/env python3	

import random as rnd

ulrs_path = './filtered_urls.txt'
train_urls_path = '../aktuality/wayback_training_urls.txt'
val_urls_path = '../aktuality/wayback_validation_urls.txt'
test_urls_path = '../aktuality/wayback_test_urls.txt'

TRAIN_SIZE, VAL_SIZE, TEST_SIZE = 80, 10, 10

def save_urls(urls, path):
	with open(path, 'w') as out_f:
		print('\n'.join(urls), file=out_f)


def main():
	with open(ulrs_path, 'r') as in_url_file:
		urls = in_url_file.read().split('\n')
	rnd.shuffle(urls)
	n_urls = len(urls)
	train_urls_size = int(n_urls * TRAIN_SIZE / 100)
	val_urls_size = int(n_urls * VAL_SIZE / 100)
	train_urls = urls[:train_urls_size]
	val_urls = urls[train_urls_size:train_urls_size+val_urls_size]
	test_urls = urls[train_urls_size+val_urls_size:]
	
	save_urls(train_urls, train_urls_path)
	save_urls(val_urls, val_urls_path)
	save_urls(test_urls, test_urls_path)	


main()



	
