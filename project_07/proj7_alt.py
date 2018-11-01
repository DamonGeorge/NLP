'''
WRITTEN FOR PYTHON 2.7
Team Member #1: Damon George
Team Member #2: Robert Brajcich
Zagmail address for team member 1: dgeorge2@zagmail.gonzaga.edu
Project 7: Generating Random N-Grams (Part 2: Bi,Tri, & Quadgrams)
Due: 10/26/2018
'''

#import for proper float division in python 2
from __future__ import division

#import necessary modules
import nltk
from nltk.corpus import brown
from collections import OrderedDict
import random
import re

def normalize_token(token):
	'''
	Takes a single token, converts it to lowercase, and remove
	any non-alphabetic characters except quotes
	'''
	token = token.lower()
	token = re.sub(r'[^a-z\']', '', token)
	return token

def keep_token(token):
	'''
	Takes a single token and returns False if it should be discarded, 
	otherwise true
	'''
	# since bad chars have already been removed, just check if empty
	return token != '' 

def parse_tokens():
	tokens = [] # holds all words
	sentence = [] # holds current sentence

	# open file and loop through each line
	with open('100-0.txt', 'r') as fin:
		for line in fin:
			tokens.append('<s>') # start of line
			sentence = [normalize_token(i) for i in line.split(' ')] # get tokens and normalize
			for word in sentence:
				if keep_token(word): # append words to list if not empty
					tokens.append(word) 
			tokens.append('</s>') # end of line

	return tokens

def count_ngrams(all_words, N):
	'''
	Counts ngrams in the all_words list of words. 
	Returns dictionary in the form (ngram_tuple : count)
	'''
	ngram_counts = {} 

	# make sure min length is met
	if len(all_words) >= N:
		for i in range(len(all_words) - (N-1)): # loop through all words
			ngram = tuple(all_words[i:i+N]) # get current ngram

			if ngram in ngram_counts: 
				ngram_counts[ngram] += 1
			else:
				ngram_counts[ngram] = 1

	return ngram_counts

def calc_ngram_frequencies(ngram_counts, total_ngrams):
	'''
	Calculates the cumulative frequencies of the ngrams.
	Returns an ordered dictionary in the form (cumulative_prob: ngram_tuple)
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

def generate_ngram(frequencies):
	'''
	Uses the ordered dict of cumulative probabilities to generate a
	random word using the Bogensberger-Johnson technique
	'''
	rand = random.random()
	for prob in frequencies.keys():
		if prob > rand:
			return frequencies[prob]

	return None

def generate_sentence(frequencies, N, show_tags, num_ngrams):
	'''
	Generates num_ngrams ngrams, capitalizes the first, and ends the
	sentence with a period. Includes sentence markers if show_tags is true.
	'''
	sentence = ""
	
	# add start sentence marker if needed
	if show_tags: 
		sentence += "<s> "

	# generate first ngram
	first_ngram = generate_ngram(frequencies)

	if N == 1: # for unigrams

		# loop through unigrams to generate
		for i in range(num_ngrams):
			# generate next unigram
			ngram = generate_ngram(frequencies)
			
			# loop until ngram doesn't include sentence marker
			while ('<s>' in ngram) or ('</s>' in ngram):
				ngram = generate_ngram(frequencies)

			# add ngram to sentence
			sentence += ' ' + ' '.join(ngram)
	
	elif N > 1: # for ngrams, not unigrams

		# loop until we have a start sentence marker and NO other sentence markers
		while (first_ngram[0] != '<s>') or ('<s>' in first_ngram[1:]) or ('</s>' in first_ngram[1:]):
			first_ngram = generate_ngram(frequencies)

		# add first ngram and capitalize
		sentence += ' ' + ' '.join(first_ngram[1:]).capitalize()

		# 
		for i in range(num_ngrams - 2):
			ngram = generate_ngram(frequencies)
			while ('<s>' in ngram) or ('</s>' in ngram):
				ngram = generate_ngram(frequencies)
			sentence += ' ' + ' '.join(ngram)
		
		last_ngram = generate_ngram(frequencies)

		while (last_ngram[N-1] != '</s>') or ('<s>' in last_ngram[:-1]) or ('</s>' in last_ngram[:-1]):
			last_ngram = generate_ngram(frequencies)

		sentence += ' ' + ' '.join(last_ngram[0:N-1])

	start = ''
	end = '.'
	if show_tags:
		start += '<s> '
		end += ' </s>'
		
	return start + sentence[1:].capitalize() + end

def get_sentence_marker_preference():
	# Prompt for yes or no 
	user_input = raw_input("Display Sentence Markers (y/n): ")
	checking_input = True
	# loop until valid input is provided
	while checking_input:
		val = user_input.strip('"\'').lower()
		if val == 'y':
			display_sentence_markers = True
			checking_input = False
		elif val == 'n':
			display_sentence_markers = False
			checking_input = False
		else:
			print("Invalid input")
			user_input = raw_input("Display Sentence Markers (y/n): ")
			checking_input = True

	return display_sentence_markers

def main():
	show_sentence_markers = get_sentence_marker_preference()

	# get lowercase list of all words
	tokens = parse_tokens()

	print("\nN-grams: ")
	for i in range(1,5):
		print("\nN = " + str(i));
		ngram_counts = count_ngrams(tokens, i)
		ngram_freqs = calc_ngram_frequencies(ngram_counts, len(tokens) - (i-1))
		for j in range(5):
			print(generate_sentence(ngram_freqs, i, show_sentence_markers, (int) (12/i)))



# entry point for the program
if __name__ == "__main__":
	main()