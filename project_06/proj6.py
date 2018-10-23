'''
WRITTEN FOR PYTHON 2.7
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Project 6: Generating Random N-Grams (Part I: Unigrams)
Due: 10/26/2018
'''

#import for proper float division in python 2
from __future__ import division

#import necessary modules
import nltk
from nltk.corpus import brown
from collections import OrderedDict
import random


def normalize_token(token):
	'''
	Takes a single token and converts it to ascii and lowercase letters
	'''
	token = token.encode('ascii')
	return token.lower()

def keep_token(token):
	'''
	Takes a single token and returns False if it should be discarded, 
	otherwise true
	'''
	return token.isalpha()

def get_all_tokens():
	'''
	Gets a list containing every token from all 
	sentences of the brown corpus (only editorials)
	'''
	sents = brown.sents(categories='editorial')
	all_words = []
	for sent in sents:
		for word in sent:
			all_words.append(word)

	return all_words

def count_types(all_words):
	'''
	Takes a list of tokens and generates a frequency map 
	in the format: {'token': occurrences}
	'''
	types = {}

	for word in all_words:
		if word in types:
			types[word] += 1
		else:
			types[word] = 1

	return types

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
	tokenized = [normalize_token(i) for i in get_all_tokens() if keep_token(i)]

	# get frequency map of how many times each type is seen
	type_counts = count_types(tokenized)

	# create cumulative probability ordered dict
	frequencies = create_frequencies(type_counts, len(tokenized))

	#print 5 randomly generated sentences
	for i in range(5):
		print(generate_sentence(frequencies))


# entry point for the program
if __name__ == "__main__":
	main()