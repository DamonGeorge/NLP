'''
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Zagmail address for team member 2: dgeorge2@zagmail.gonzaga.edu
Project 3: Extracts tokenized inaugural addresses into files and
	finds the frequency of a word in each address
Due: 9/14/2018
'''

#import necessary libraries
from nltk.corpus import inaugural
import matplotlib.pyplot as plt
import re


def write_address_file(address):
	'''
	Writes all of the provided inaugural address to a new file.
	'''

	#create new txt file
	with open(address, 'w') as fout:
		#join all the words in each  sentence 
		for sent in inaugural.sents(address):
			sent = ' '.join(sent)
			fout.write(sent + '\n')

def tokenize_address(address):
	'''
	Reads the specified address from its txt file and 
	returns a new string that is the address converted to lower case
	with all non-word characters removed. Spaces are not removed. 
	'''

	#read the address and remove new lines
	with open(address, 'r') as fin:
		string = re.sub('\n',' ', fin.read())
		
	#lower and substitute all non-word characters with spaces
	string = string.lower()
	new_str = re.sub(r'[^a-z ]', ' ', string)
	return new_str


def main():
	'''
	Gets a word from the user. Writes out all inaugural addresses from nltk to their own files.
	Then this program tokenizes all addresses into a singular file.
	From this file, the program counts the number of instances of the given word,
	and plots this count over each year of inaugurual addresses. 
	'''

	#get the word to search
	search = input("Enter word to search: ")
	search.strip('"\'') # remove quotes if grader tries to use them
	search.lower();		# lower since tokenizing lowers all letters in the addresses

	#get files names from nltk library
	file_ids = inaugural.fileids()
	
	#lists to hold years and the frequency counts to use in the graph
	years = []
	counts = []

	#create output file
	with open('proj3.txt', 'w') as fout:
		#loop through all inaugural addresses
		for address in file_ids:
			#add year to list - the year is the first 4 characters of each address title
			years.append(int(address[:4]))

			#write each address to file
			write_address_file(address)

			#tokenize each address, append a newline to separate addresses, and write to output
			string = tokenize_address(address)
			string = string + '\n'
			fout.write(string)
	
	#open output file 
	with open('proj3.txt', 'r') as fin:
		#loop through each address
		for address in fin:
			#split into words 
			words = address.split();

			#initial frequency is 0
			count = 0

			#Increment the count if each word matches the input
			for word in words:
				if word == search:
					count = count + 1

			#append count to the list 
			counts.append(count)

	#plot the word count vs year
	plt.plot(years,counts)
	plt.show()


if __name__ == "__main__":
	main()
