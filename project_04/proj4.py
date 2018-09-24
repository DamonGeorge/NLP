'''
WRITTEN FOR PYTHON 3
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Project 4: Implements the Soundex algorithm as a finite state transducer.
		   Accepts an input string and outputs the encoded form.
Due: 9/28/2018
'''

#import required modules
import sys
import re


def get_input_str():
	'''
	If an input string was supplied in cmd line, return it. Otherwise print 
	an error message and exit the program.
	'''
	if len(sys.argv) is not 2:
		print('ERROR: please provide a valid input string')
		print('       as a command line argument')
		exit()
	else:
		return sys.argv[1]


def soundex_replace_chars(in_str):
	'''
	Implements step 1 of the soundex algorithm, replacing groups of similar
	letters with a corresponding number (except the first letter)
	'''
	in_str = re.sub(r'(?<=.)[bfpv]', '1', in_str);
	in_str = re.sub(r'(?<=.)[cgjkqsxz]', '2', in_str);
	in_str = re.sub(r'(?<=.)[dt]', '3', in_str);
	in_str = re.sub(r'(?<=.)[l]', '4', in_str);
	in_str = re.sub(r'(?<=.)[mn]', '5', in_str);
	in_str = re.sub(r'(?<=.)[r]', '6', in_str);

	return in_str


def soundex_collapse_nums(in_str):
	'''
	Implements step 2 of the soundex algorithm, collapsing any repeated numbers
	'''
	return re.sub(r'([0-9])\1+', r'\1', in_str)


def soundex_remove_chars(in_str):
	'''
	Implements step 3 of the soundex algorithm, removing any occurrences of
	certain characters except for the first letter of the name. Due to 
	reordering of soundex algorithm, this function just removes all characters
	that are not numeric digits (except it does not remove the first letter)

	NOTE: this step is moved from the standard soundex step 1 to be step 3 in 
		  order to simplify step 2 above, since the numbers should only 
		  collapse if they are adjacent IN THE ORIGINAL STRING.
	'''
	return re.sub(r'(?<=.)[^0-9]', '', in_str);


def soundex_format_result(in_str):
	'''
	Implements step 4 of the soundex algorithm, padding or cutting off
	the result string to adhere to the format LETTER DIGIT DIGIT DIGIT
	'''
	if len(in_str) > 4:
		return in_str[:4]
	else:
		return in_str + '0'*(4-len(in_str))


def main():

	# get command line input name; make it lower case (except first letter)
	cur_str = get_input_str().lower()
	cur_str = cur_str[0].upper() + cur_str[1:] 

	# print string before encoding
	print(cur_str, end=' -> ')	

	# apply soundex transducer (step order altered to simplify program)
	cur_str = soundex_replace_chars(cur_str) # step 1
	cur_str = soundex_collapse_nums(cur_str) # step 2
	cur_str = soundex_remove_chars(cur_str) # step 3
	cur_str = soundex_format_result(cur_str) # step 4

	# print fully encoded string
	print(cur_str)


if __name__ == "__main__":
	main()
