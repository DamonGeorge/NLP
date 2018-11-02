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

START_TAG = '<s>'
END_TAG = '</s>'

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

def parse_tokens():
	tokens = [] # holds all words
	sentence = [] # holds current sentence

	# open file and loop through each line
	with open('100-0.txt', 'r') as fin:
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
	Returns dictionary in the form (ngram_tuple : count) and total count of ngrams
	'''
	ngram_counts = {} 
	total_count = 0

	# make sure min length is met
	if len(all_words) >= N:
		for i in range(len(all_words) - (N-1)):
			ngram = tuple(all_words[i:i+N]) # get current ngram

			# only record tags that don't have sentence markers in the middle
			if START_TAG not in ngram[1:] \
				and END_TAG not in ngram[:-1] \
				and not (START_TAG == ngram[0] and END_TAG == ngram[N-1]):

				# increment count and update count in dict
				total_count += 1 
				if ngram in ngram_counts: 
					ngram_counts[ngram] += 1
				else:
					ngram_counts[ngram] = 1

	return ngram_counts, total_count

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

	# generate first ngram
	first_ngram = generate_ngram(frequencies)

	if N == 1: # for unigrams
		# loop through unigrams to generate
		for i in range(num_ngrams):
			# generate next unigram
			ngram = generate_ngram(frequencies)
			
			# loop until ngram doesn't include sentence marker
			while (START_TAG in ngram) or (END_TAG in ngram):
				ngram = generate_ngram(frequencies)

			# add ngram to sentence
			sentence += ' ' + ' '.join(ngram)
	
	elif N > 1: # for ngrams, not unigrams
		# loop until we have a start sentence marker
		while first_ngram[0] != START_TAG:
			first_ngram = generate_ngram(frequencies)

		# add first ngram and capitalize
		sentence += ' ' + ' '.join(first_ngram[1:])

		# add ngrams in the middle of the sentence
		for i in range(num_ngrams - 2):
			ngram = generate_ngram(frequencies)

			# loop until ngram has no sentence markers, then add to sentence
			while (START_TAG in ngram) or (END_TAG in ngram):
				ngram = generate_ngram(frequencies)
			
			sentence += ' ' + ' '.join(ngram)
		
		# last ngram
		last_ngram = generate_ngram(frequencies)

		# loop until we have end sentence marker and add to sentence
		while last_ngram[N-1] != END_TAG:
			last_ngram = generate_ngram(frequencies)

		sentence += ' ' + ' '.join(last_ngram[0:N-1])

	# start and end to string
	start = ''
	end = '.'
	if show_tags:
		start += START_TAG + ' '
		end += ' ' + END_TAG
		
	return start + sentence[1:].capitalize() + end

def get_sentence_marker_preference():
	'''
	Get user's preference as to whether to display sentence markers.
	Returns boolean value
	'''
	# Prompt for yes or no 
	user_input = raw_input("Display Sentence Markers (y/n): ")
	checking_input = True
	
	# loop until valid input is provided
	while checking_input:
		val = user_input.strip('"\'').lower() # get and clean input
		
		# if invalid input try again, otherwise return choice
		if val != 'y' and val != 'n': 
			print("Invalid input")
			user_input = raw_input("Display Sentence Markers (y/n): ")
			checking_input = True
		else:
			display_sentence_markers = (val == 'y')
			checking_input = False

	return display_sentence_markers

def main():
	# get user's show marker preference
	show_sentence_markers = get_sentence_marker_preference()

	# get lowercase list of all words
	tokens = parse_tokens()

	print("\nN-grams: ")

	# loop through unigrams to quadgrams
	for i in range(1,5):
		# print ngram number
		print("\nN = " + str(i));

		# count the ngrams
		ngram_counts, total_count = count_ngrams(tokens, i)

		# calc the frequencies
		ngram_freqs = calc_ngram_frequencies(ngram_counts, total_count)

		# generate 5 line
		for j in range(5):
			print(generate_sentence(ngram_freqs, i, show_sentence_markers, (int) (12/i)))



# entry point for the program
if __name__ == "__main__":
	main()