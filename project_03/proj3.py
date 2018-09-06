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

	#create a list containing all lower case characters
	good_chars = [chr(value) for value in range(ord('a'),ord('z') + 1,1)]
	good_chars.append(' ')
   
	new_str = ''
	for ch in string:
		if ch in good_chars:
			new_str = new_str + ch
	

	#or just use:
	#re.sub(r'[^a-z ]', '', string)
	return new_str



def main():
	#get files
	file_ids = inaugural.fileids()

	#open output file
	with open('proj3.txt', 'w') as fout:
		#loop through all inaugural addresses
		for address in file_ids:
			#write each address to file
			write_address_file(address)
			#tokenize each address, prepend the year, append a newline, and write to output
			string = tokenize_address(address)
			string = address[:4] + ' ' + string + '\n'
			fout.write(string)

	search = 'people'
	years = []
	counts = []
	with open('proj3.txt', 'r') as fin:
		for address in fin:
			words = address.split(' ');
			year = int(words[0])
			years.append(year)
			count = 0
			for word in words[1:]:
				if word == search:
					count = count + 1
			counts.append(count)

	print(years)
	plt.plot(years,counts)
	plt.show()






if __name__ == "__main__":
	main()