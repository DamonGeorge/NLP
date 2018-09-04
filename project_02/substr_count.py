'''
Team Member #1: Robert Brajcich
Team Member #2: Damon George
Zagmail address for team member 1: rbrajcich@zagmail.gonzaga.edu
Zagmail address for team member 2: dgeorge2@zagmail.gonzaga.edu
Project 2: This program asks for a file and substring, and prints the
		   number of occurrences of said substring in the file.
Due: 9/7/2018
'''

# returns the number of times substr is found in target_str
def count_occurrences(substr, target_str):
	
	# if the substring is larger than the main string, for sure no matches 
	if len(target_str) < len(substr):
		return 0

	result = 0

	# loop through each letter and add a count if the substring exists starting there
	for search_idx in range(1 + len(target_str) - len(substr)):
		result += 1 if substr_exists_at_index(search_idx, substr, target_str) else 0

	return result

# returns True if the substring exists at specified location in target_str; otherwise False
def substr_exists_at_index(start_idx, substr, target_str):

	# look at each letter and return false if any of them don't match
	for char_idx in range(len(substr)):
		if target_str[start_idx + char_idx] is not substr[char_idx]:
			return False

	# otherwise return True
	return True

# reads the entire contents of the file specified and returns it as a string
# NOTE: throws FileNotFoundError if the file does not exist
def read_whole_file(filename):
	with open(filename, 'r') as f:
		return f.read()

def main():

	# Prompt for a valid file to read and read it
	filename = input("Enter file to parse: ")
	trying_file = True
	while trying_file:
		try:
			file_contents = read_whole_file(filename)
			trying_file = False
		except FileNotFoundError:
			filename = input("File not found. Try a different file: ")

	# Now prompt for substring
	substring = input("Enter substring to find: ")
	while len(substring) < 1:
		substring = input("Please enter a valid substring: ")

	# Calculate the result and output it
	num_occurrences = count_occurrences(substring, file_contents)
	print("----------")
	print("Looking for {} in {}:".format(substring, filename))
	print("{} occurrences found!".format(num_occurrences))


if __name__ == "__main__":
	main()
