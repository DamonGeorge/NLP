'''
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Zagmail address for team member 2: dgeorge2@zagmail.gonzaga.edu
Project 3: Extracts tokenized inaugural addresses into a serialized file and
	finds the frequency of a word in each address
Due: 9/14/2018
'''

#import necessary libraries
from nltk.corpus import inaugural
import matplotlib.pyplot as plt
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

	#lists to hold years and the frequency counts to use in the graph
	years = []
	counts = []

	#loop through all inaugural addresses
	for address in file_ids:
		#add year to list - the year is the first 4 characters of each address title
		years.append(int(address[:4]))

		#read the address into a string of newline separated sentences
		string = read_address(address)

		#tokenize each address into a list of lowercase words
		words = tokenize(string)

		#append the tokenized address to the master list
		tokenized_addresses.append(words)

	#serialize list of addresses to pickle file
	with open('proj3.pkl', 'wb') as fout:
		pickle.dump(tokenized_addresses, fout)
	
	#Part 2: Load pickle data, search word, and plot frequency
	#=============================================

	#get the word to search
	search = input("Enter word to search: ")
	search.strip('"\'') # remove quotes if grader tries to use them
	search.lower();		# lower since tokenizing lowers all letters in the addresses

	with open('proj3.pkl', 'rb') as fin:
		parsed_addresses = pickle.load(fin)


	#loop through each address
	for address in parsed_addresses:
		#initial frequency is 0
		count = 0

		#Increment the count if each word matches the input
		for word in address:
			if word == search:
				count = count + 1

		#append count to the list 
		counts.append(count)

	#plot the year vs word count
	plt.plot(counts,years)
	plt.show()


if __name__ == "__main__":
	main()
