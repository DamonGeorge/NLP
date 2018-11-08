'''
WRITTEN FOR PYTHON 2.7
Team Member #1: Damon George
Team Member #2: Robert Brajcich
Zagmail address for team member 1: dgeorge2@zagmail.gonzaga.edu
Project 7b: Generating Random N-Grams (Part 2: Bi,Tri, & Quadgrams)
Due: 11/09/2018
'''
#import necessary modules
from collections import OrderedDict
import random
import pickle

# line markers
START_TAG = '<s>'
END_TAG = '</s>'
# filenames
PICKLE_FILENAME = 'proj7b.pkl'

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

def generate_sentence(frequencies, N, num_ngrams):
	'''
	Generates num_ngrams ngrams, capitalizes the first, and ends the
	sentence with a period. Includes sentence markers if show_tags is true.
	'''
	sentence = ""

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
		# generate first ngram
		first_ngram = generate_ngram(frequencies)

		# loop until we have a start sentence marker
		while first_ngram[0] != START_TAG:
			first_ngram = generate_ngram(frequencies)

		# add first ngram 
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

		# add last ngram
		sentence += ' ' + ' '.join(last_ngram[0:N-1])
		
	return sentence[1:].capitalize() + '.'  # capitalize and add period

def main():
	print('Loading pickle file...')

	#Load pickled list of addresses
	with open(PICKLE_FILENAME, 'rb') as fin:
		all_ngram_freqs = pickle.load(fin)

	print("\nGenerating N-grams: ")

	# loop through unigrams to quadgrams
	for i in range(1,5):
		# print ngram number
		print("\nN = " + str(i));

		# generate 5 line
		for j in range(5):
			print(generate_sentence(all_ngram_freqs[i], i, (int) (12/i)))


# entry point for the program
if __name__ == "__main__":
	main()