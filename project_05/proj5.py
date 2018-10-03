'''
WRITTEN FOR PYTHON 3
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Project 4: Computes the minimum edit distance between two input strings and 
		displays the alignment of the strings.
Due: 9/28/2018
'''

#import required modules
import sys


def print_matrix(matrix):
	rows = len(matrix)
	cols = len(matrix[0])

	for i in range(rows):
		for j in range(cols):
			print(f'{matrix[i][j]:2}, ', end='')
		print('')


class Operation:
	'''
	Constants for Operation Type. Used in the operation matrices
	'''
	SUBSTITUTION = 0
	INSERT = 1
	DELETE = 2

def insert_cost(char):
	'''
	Insert Cost Function: returns constant of 1
	'''
	return 1;

def delete_cost(char):
	'''
	Delete Cost Function: returns constant of 1
	'''
	return 1;

def sub_cost(char1, char2):
	'''
	Substituion Cost Function: returns 0 if characters equal, 2 otherwise
	'''
	if char1 == char2:
		return 0
	else:
		return 2

def get_matrix_dimensions(matrix):
	'''
	Returns the dimensions of the provided 2d list as rows, cols
	'''
	return len(matrix), len(matrix[0])


def get_input_str():
	'''
	If the 2 input strings were supplied in cmd line, return them. Otherwise print 
	an error message and exit the program.
	'''
	if len(sys.argv) is not 3:
		print('ERROR: please provide valid input strings')
		print('       as a command line arguments')
		exit()
	else:
		return sys.argv[1], sys.argv[2]


def init_matrices(edit_dist_matrix, operation_matrix, source, target):
	'''
	Performs initial calculations on the provided matrices.
	This fills the first row and col of both matrices. 
	
	Parameters:
		edit_dist_matrix: 2d list used to calculate min edit distance
		operation_matrix: 2d list used to hold all operations while calculating 
			min edit distance
		source: source string
		target: target string

	Returns:
		nothing
	'''

	rows, cols = get_matrix_dimensions(edit_dist_matrix)

	# For first col, fill with delete costs
	for i in range(1,rows):
		edit_dist_matrix[i][0] = edit_dist_matrix[i-1][0] + delete_cost(source[i-1]);
		operation_matrix[i][0] = Operation.DELETE;
	
	# for first row, fill with insert costs
	for j in range(1, cols):
		edit_dist_matrix[0][j] = edit_dist_matrix[0][j-1] + insert_cost(target[j-1]);
		operation_matrix[0][j] = Operation.INSERT;


def calc_matrices(edit_dist_matrix, operation_matrix, source, target):
	'''
	Calculates all cells of the two provided matrices using the 
	minimum edit distance algorithm. The two matrices must have 
	already been initialized using the init_matices() function.
	
	Parameters:
		edit_dist_matrix: 2d list used to calculate min edit distance
		operation_matrix: 2d list used to hold all operations while calculating 
			min edit distance
		source: source string
		target: target string

	Returns:
		nothing
	'''

	rows, cols = get_matrix_dimensions(edit_dist_matrix)

	# loop through all cells
	for i in range(1,rows):
		for j in range(1, cols):
			# calculate insert, delete and sub costs
			insert = edit_dist_matrix[i][j-1] + insert_cost(target[j-1])
			delete = edit_dist_matrix[i-1][j] + delete_cost(source[i-1])
			sub = edit_dist_matrix[i-1][j-1] + sub_cost(source[i-1], target[j-1])

			# set value in main matrix to be minimum of the 3 operations
			edit_dist_matrix[i][j] = min(insert, delete, sub)

			# check which value was used, and set the corresponding operation 
			# in the operation matrix
			if edit_dist_matrix[i][j] == sub :
				operation_matrix[i][j] = Operation.SUBSTITUTION
			elif edit_dist_matrix[i][j] == insert :
				operation_matrix[i][j] = Operation.INSERT
			else:
				operation_matrix[i][j] = Operation.DELETE


def print_alignment(operation_matrix, source, target):
	'''
	Prints the pretty alignment of the source and target as shown
	in Jurafsky and Martin
	
	Parameters:
		operation_matrix: 2d list used to hold all operations used to 
			calculate min edit distance matrix
		source: source string
		target: target string

	Returns:
		nothing - just prints alignment to screent
	'''

	rows, cols = get_matrix_dimensions(operation_matrix)

	# useful indices: start our search at cell holding min edit distance
	i = rows-1
	j = cols-1

	# indices to hold where in source and target we are
	src_index = len(source) - 1;
	tar_index = len(target) - 1;

	# the 4 lines of the alignment printout
	line1 = ""
	line2 = ""
	line3 = ""
	line4 = ""
	
	# loop until we have reached the start of the operation matrix
	while(i != 0 or j != 0):
		# current operation
		current = operation_matrix[i][j]

		# add pipe for each operation
		line2 += "|"

		if current == Operation.SUBSTITUTION:
			# print char from both source and target
			line1 += source[src_index]
			line3 += target[tar_index]

			# if the two chars are not equal, than a substitution was actually made
			if source[src_index] != target[tar_index]:
				line4 += "s"
			else :
				line4 += " "
			src_index -= 1
			tar_index -= 1

			# move diagonally through matrix
			i = i - 1
			j = j - 1
		elif current == Operation.INSERT:
			# insert * into line 1 and print char from target
			line1 += "*"
			line3 += target[tar_index]
			tar_index -= 1
			line4 += "i"

			# move left through matrix
			j = j - 1
		elif current == Operation.DELETE:
			# print char from source and insert * into line 3
			line1 += source[src_index]
			src_index -= 1
			line3 += "*"
			line4 += "d"

			# move up through matrix
			i = i - 1
	
	# print lines reversed
	print(line1[::-1])
	print(line2)
	print(line3[::-1])
	print(line4[::-1])


def main():
	# get command line inputs: source and target strings
	source, target = get_input_str();

	# get length of source and target
	m = len(source)
	n = len(target)

	# create the main matrix and an additional one to hold the alignment information
	# m+1 rows and n+1 cols
	min_edit_dist_matrix = [[0] * (n+1) for i in range(m+1)]
	operation_matrix = [[0] * (n+1) for i in range(m+1)]

	# first steps in filling the matrices
	init_matrices(min_edit_dist_matrix, operation_matrix, source, target)

	# fill in the rest of the two matrices
	calc_matrices(min_edit_dist_matrix, operation_matrix, source, target)

	# print everything
	print("alignment: ")
	print_matrix(min_edit_dist_matrix)
	print(f"Minimum Edit Distance: {min_edit_dist_matrix[m][n]}")
	print('')
	print("Alignment: ")
	print_alignment(operation_matrix, source, target)
	print('')


if __name__ == "__main__":
	main()
