'''
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Zagmail address for team member 2: dgeorge2@zagmail.gonzaga.edu
Project 3: 
Due: 9/14/2018
'''

from nltk.corpus import inaugural
import matplotlib.pyplot as plt
import re

def write_address_file(address):
	with open(address, 'w') as fout:
		#join all the words in each  sentence 
		for sent in inaugural.sents(address):
			sent = ' '.join(sent)
			fout.write(sent + '\n')

def tokenize_address(address):
	
	with open(address, 'r') as fin:
		string = re.sub('\n',' ', fin.read())
		
	string = string.lower()
	new_str = re.sub(r'[^a-z ]', ' ', string)
	return new_str


def main():
	search = input("Enter word to search: ")
	search.strip('"\'') # remove quotes if grader tries to use them
	search.lower();

	#get files
	file_ids = inaugural.fileids()
	
	years = []
	counts = []

	#open output file
	with open('proj3.txt', 'w') as fout:
		#loop through all inaugural addresses
		for address in file_ids:
			#add year to list
			years.append(int(address[:4]))
			#write each address to file
			write_address_file(address)
			#tokenize each address, prepend the year, append a newline, and write to output
			string = tokenize_address(address)
			string = string + '\n'
			fout.write(string)
	
	with open('proj3.txt', 'r') as fin:
		for address in fin:
			words = address.split(' ');
			print(words[:10])
			count = 0
			for word in words:
				if word == search:
					count = count + 1
			counts.append(count)

	plt.plot(years,counts)
	plt.show()






if __name__ == "__main__":
	main()