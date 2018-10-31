'''
WRITTEN FOR PYTHON 3
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Project 3: Extracts tokenized inaugural addresses from pickle file ('proj3.pkl') 
	and finds the frequency of a word in each address
Due: 9/14/2018
'''

#import necessary libraries
import matplotlib.pyplot as plt
import pickle


def main():

	#Load pickled list of addresses
	with open('proj3.pkl', 'rb') as fin:
		parsed_addresses = pickle.load(fin)

	#get the word to search
	search = input("Enter word to search: ")
	search.strip('"\'') # remove quotes if grader tries to use them
	search.lower();		# lower since tokenizing lowers all letters in the addresses

	#dict to hold year:count
	word_frequency = {}

	#loop through each address
	for address in parsed_addresses:
		#initial frequency is 0
		count = 0

		#first word is the address file title
		#parse year from first four letters of the title
		year = int(address[0][:4])

		#Increment the count if each word matches the input
		for word in address[1:]:
			if word == search:
				count = count + 1

		#add new values to dict
		word_frequency[year] = count

	#plot the year vs word count
	plt.plot(word_frequency.keys(), word_frequency.values())
	plt.xlabel('Year')
	plt.ylabel('Word Count')
	plt.show()


if __name__ == "__main__":
	main()
