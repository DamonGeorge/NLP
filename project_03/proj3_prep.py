'''
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Project 3: Extracts tokenized inaugural addresses into a pickle file
Due: 9/14/2018
'''

#import necessary libraries
from nltk.corpus import inaugural
import re
import pickle

def read_address(address):
	'''
	Reads the given nltk inaugural address to a string
	'''
	full_address = ""

	#join all the words in each  sentence 
	for sent in inaugural.sents(address):
		sent = ' '.join(sent)
		full_address = full_address + sent + '\n'

	return full_address
	

def tokenize(string):
	'''
	Returns a list of words parsed from the string with all non-word characters removed.
	'''
	#lower and substitute all non-word characters with spaces
	string = string.lower()
	new_str = re.sub(r'[^a-z ]', ' ', string)

	words = new_str.split()

	return words


def main():

	#Part 1: load inaugural addresses, tokenize, and serialize to pickle file
	#=============================================
	
	#get files names from nltk library
	file_ids = inaugural.fileids()
	
	#list to all hold tokenized addresses
	tokenized_addresses = []

	#loop through all inaugural addresses
	for address in file_ids:

		#read the address into a string of newline separated sentences
		string = read_address(address)

		#tokenize each address into a list of lowercase words
		words = tokenize(string)

		#add address title to beginning of address
		words.insert(0, address);

		#append the tokenized address to the master list
		tokenized_addresses.append(words)

	#serialize list of addresses to pickle file
	with open('proj3.pkl', 'wb') as fout:
		pickle.dump(tokenized_addresses, fout)


if __name__ == "__main__":
	main()
