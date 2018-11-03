'''
WRITTEN FOR PYTHON 2.7
Team Member #1: Damon George
Team Member #2: Robert Brajcich
Zagmail address for team member 1: dgeorge2@zagmail.gonzaga.edu
Project 7a: Generating Random N-Grams (Part 2: Bi,Tri, & Quadgrams)
Due: 11/09/2018
'''

#import for proper float division in python 2
from __future__ import division

#import necessary modules
from collections import OrderedDict
import re
import pickle

# line markers
START_TAG = '<s>'
END_TAG = '</s>'
# filenames
TEXT_FILENAME = 'shakespeare.txt'
PICKLE_FILENAME = 'proj7.pkl'

def normalize_line(line):
	'''
	Takes a string, converts it to lowercase, and removes
	any non-alphabetic characters except quotes
	'''
	line = line.lower()
	line = re.sub(r'[^a-z\' ]', '', line)
	return line

def keep_token(token):
	'''
	Takes a single token and returns False if it should be discarded, 
	otherwise true
	'''
	# since bad chars have already been removed, just check if empty
	return bool(token)

def parse_tokens(filename):
	'''
	Tokenizes the text file into a list of clean words with each line
	starting with START_TAG and ending with END_TAG.
	'''
	tokens = [] # holds all words
	sentence = [] # holds current sentence

	# open file and loop through each line
	with open(filename, 'r') as fin:
		for line in fin:
			sentence = normalize_line(line) # remove bad characters
			sentence = [i for i in sentence.split(' ') if keep_token(i)] # get tokens and remove bad ones

			if len(sentence) > 0 : # if sentence is not empty
				tokens.append(START_TAG) # start of line
				tokens.extend(sentence) # tokens
				tokens.append(END_TAG) # end of line

	return tokens

def count_ngrams(all_words, N):
	'''
	Counts ngrams in the all_words list of words. 
	Returns dictionary in the form {ngram_tuple : count} and total count of ngrams
	'''
	ngram_counts = {} 
	total_count = 0

	# make sure min length is met
	if len(all_words) >= N:
		for i in range(len(all_words) - (N-1)):
			ngram = tuple(all_words[i:i+N]) # get current ngram

			# only record tags that don't have sentence markers in the middle
			# and don't have both the start and end tags
			if START_TAG not in ngram[1:] \
				and END_TAG not in ngram[:-1] \
				and not (START_TAG == ngram[0] and END_TAG == ngram[N-1]):

				# increment total count and update ngram count in dict
				total_count += 1 
				if ngram in ngram_counts: 
					ngram_counts[ngram] += 1
				else:
					ngram_counts[ngram] = 1

	return ngram_counts, total_count

def calc_ngram_frequencies(ngram_counts, total_ngrams):
	'''
	Calculates the cumulative frequencies of the ngrams.
	Returns an ordered dictionary in the form {cumulative_prob: ngram_tuple}
	'''
	cumulative_count = 0
	frequencies = OrderedDict()

	# for each type, calculate frequency -> cumulative probability,
	# and add to the ordered dict
	for ngram in ngram_counts:
		ngram_freq = ngram_counts[ngram] / total_ngrams
		cumulative_count += ngram_freq
		frequencies[cumulative_count] = ngram

	return frequencies


def main():
	tokens = parse_tokens(TEXT_FILENAME) # get lowercase list of all words

	all_ngram_freqs = {} # dict to hold {N : dict of ngram freqs}

	print('Counting Ngrams...')

	# loop through unigrams to quadgrams
	for i in range(1,5):
		# count the ngrams
		ngram_counts, total_count = count_ngrams(tokens, i)

		# calc the frequencies
		ngram_freqs = calc_ngram_frequencies(ngram_counts, total_count)

		# add to master list
		all_ngram_freqs[i] = ngram_freqs

	print('Pickling Ngram Frequencies...')

	# serialize list of addresses to pickle file
	with open(PICKLE_FILENAME, 'wb') as fout:
		pickle.dump(all_ngram_freqs, fout)

	print ('Done!')


# entry point for the program
if __name__ == "__main__":
	main()