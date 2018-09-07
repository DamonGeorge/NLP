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

def main():
	string = "hey , what's up dude?...."
	string = re.sub(r'[^a-z_]', ' ', string)
	print(string)





if __name__ == "__main__":
	main()