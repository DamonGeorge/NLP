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
	Takes a single token and converts it to ascii and lowercase letters
	'''
	token = token.encode('ascii')
	token = token.lower()
	token = re.sub(r'[^a-z\']', '', token)
	return token

def keep_token(token):
	'''
	Takes a single token and returns False if it should be discarded, 
	otherwise true
	'''
	#return re.search(r'[a-z\']', token
	return token != ''

def parse_tokens():
	tokens = []
	sentence = []

	# open file and loop through each line
	with open('100-0.txt', 'r') as fin:
		for line in fin:
			tokens.append('<s>') # start of line
			sentence = [normalize_token(i) for i in line.split(' ')] # get tokens and normalize
			for word in sentence:
				if keep_token(word):
					tokens.append(word)
			tokens.append('</s>') # end of line

	return tokens


def count_ngrams(all_words, N):
	'''
	Counts ngrams - NOT for unigrams
	'''
	ngram_counts = {} # dict of dicts of the form {(n-1 first words tuple) : {lasttoken : occurences}}
	first_words_counts = {} # dict of {(n-1 first words tuple) : occurences}
	num_unique_ngrams = 0 # total number of unique ngrams
	sentence_start_ngrams = {} # dict to hold ngrams that start with <s> -> {(n-1 last words tuple) : occurences}
	num_sentence_start_ngrams = 0

	#CHECK IF LENGTH of all_words is >= N
	if len(all_words) >= N:
		for i in range(len(all_words) - (N-1)):
			first_words = tuple(all_words[i:i+N-1]); # first n-1 words
			last_word = all_words[i+N-1] # new word

			# add to ngram_counts
			if first_words in ngram_counts:
				if last_word in ngram_counts[first_words]:
					ngram_counts[first_words][last_word] += 1;
				else:
					ngram_counts[first_words][last_word] = 1;
					num_unique_ngrams += 1
			else:
				ngram_counts[first_words] = {}
				ngram_counts[first_words][last_word] = 1;
				num_unique_ngrams += 1

			# add count to total word counts dict
			if first_words in first_words_counts:
				first_words_counts[first_words] += 1
			else:
				first_words_counts[first_words] = 1

			# possibly add to dict of ngrams that start with <s> -> OR JUST WHEN GENERATING LOOP UNTIL NGRAM IS CHOSEN THAT STARTS WITH <s>????
			if first_words[0] == '<s>':
				num_sentence_start_ngrams += 1
				last_words = tuple(all_words[i+1:i+N])
				if last_words in sentence_start_ngrams:
					sentence_start_ngrams[last_words] += 1
				else:
					sentence_start_ngrams[last_words] = 1

	return ngram_counts, first_words_counts, sentence_start_ngrams, num_sentence_start_ngrams
#ALSO NEED DICT TO HOLD COUNTS OF NGRAMS THAT ALL START WITH <s> !!!!!!!!!!

#def count_unigrams(all_words):
	# insert robert's code here

def calc_ngram_frequencies(ngram_counts, first_words_counts):
	#SORT EACH INNER DICT???????????????

	ngram_cumulative_freqs = {} 

	for first_words in ngram_counts:
		cumulative_count = 0
		counts = ngram_counts[first_words] #dict of counts for each ngram
		ngram_cumulative_freqs[first_words] = OrderedDict() # create new ordered dict to hold cumulative frequences

		for last_word in counts:
			ngram_freq = counts[last_word] / first_words_counts[first_words]
			cumulative_count += ngram_freq
			ngram_cumulative_freqs[first_words][cumulative_count] =  last_word

	return ngram_cumulative_freqs

def calc_start_ngram_frequencies(sentence_start_ngrams, ngram_cumulative_freqs):
	sentence_start_ngram_cumulative_freqs = OrderedDict()
	cumulative_count = 0

	for ngram in sentence_start_ngrams:
		freq = sentence_start_ngrams[ngram] / ngram_cumulative_freqs
		cumulative_count += freq
		sentence_start_ngram_cumulative_freqs[cumulative_count] = ngram

	return sentence_start_ngram_cumulative_freqs

def create_frequencies(type_counts, total_tokens):
	'''
	Using a frequency map and total token count, generates an ordered
	dict in the format {cumulative_probability: 'token'}
	'''
	cumulative_count = 0
	frequencies = OrderedDict()

	# for each type, calculate frequency -> cumulative probability,
	# and add to the ordered dict
	for typ in type_counts.iterkeys():
		type_freq = type_counts[typ] / total_tokens
		cumulative_count += type_freq
		frequencies[cumulative_count] = typ

	return frequencies

def generate_word(frequencies):
	'''
	Uses the ordered dict of cumulative probabilities to generate a
	random word using the Bogensberger-Johnson technique
	'''
	point = random.random()
	for prob in frequencies.keys():
		if prob > point:
			return frequencies[prob]

	return None

def generate_sentence(frequencies):
	'''
	Generates 10 random words, capitalizes the first, and ends the
	sentence with a period
	'''
	sentence = generate_word(frequencies).title()
	for i in range(9):
		sentence += ' ' + generate_word(frequencies)

	sentence += '.'
	return sentence

def main():
	# get lowercase list of all words
	tokens = parse_tokens()

	print tokens

	counts, main_counts, start_ngrams, start_count = count_ngrams(tokens, 3)

	print start_ngrams

	ngram_freqs = calc_ngram_frequencies(counts, main_counts)

	print ""
	print "Cumulative:"
	print ngram_freqs

	sent_start_freqs = calc_start_ngram_frequencies(start_ngrams, start_count)
	print sent_start_freqs

	# get frequency map of how many times each type is seen
	#type_counts = count_types(tokenized)

	# create cumulative probability ordered dict
	#frequencies = create_frequencies(type_counts, len(tokenized))

	#print 5 randomly generated sentences
	#for i in range(5):
	#	print(generate_sentence(frequencies))


# entry point for the program
if __name__ == "__main__":
	main()