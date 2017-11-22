# doc.py

import re

poster_file_name = 'poster.txt'
oral_file_name = 'oral.txt'
output_file_name = 'author_list_oral_and_poster.txt'

def remove_spaces(authors):
	new_authors = []
	for author in authors:
		author = author.strip()
		new_authors.append(author)
	return new_authors

# ----------------------------------
# ----------------------------------
# --------poster--------------------
# ----------------------------------
# ----------------------------------

# open file
with open(poster_file_name) as file_obj_pos:
	contents = file_obj_pos.read()

# first split
splited_contents = re.split(r'\n\n\n',contents)

for splited_content in splited_contents:
	splited_content = splited_content.rstrip()

splited_contents[-1] = splited_contents[-1].rstrip()

# second split
further_splited_contents = []
for splited_content in splited_contents:
	further_splited_content = re.split(r'\n',splited_content)
	further_splited_contents.append(further_splited_content)

# remove abstract
for further_splited_content in further_splited_contents:
	del further_splited_content[-1]

# remove title
for further_splited_content in further_splited_contents:
	del further_splited_content[1]

# remove bracket-contents(twice)
for further_splited_content in further_splited_contents:
	further_splited_content[1] = re.sub(r'\((.*?)\)','&',further_splited_content[1])
for further_splited_content in further_splited_contents:
	further_splited_content[1] = re.sub(r'\((.*?)\)','&',further_splited_content[1])
	
# seperate authors
for further_splited_content in further_splited_contents:
	authors = re.split(r'&|;|,|\band\b',further_splited_content[1])#
	for author in authors:
		if len(author) <= 4:
			authors.remove(author)
	further_splited_content[1] = authors

# remove spaces in author names
for further_splited_content in further_splited_contents:
	further_splited_content[1] = remove_spaces(further_splited_content[1])

## print all
#for further_splited_content in further_splited_contents:
	#for item in further_splited_content:
		#print(item)
		
# ----------------------------------
# ----------------------------------
# --------oral----------------------
# ----------------------------------
# ----------------------------------

# open file
with open(oral_file_name) as file_obj_oral:
	oral_contents = file_obj_oral.read()

# remove time
oral_contents = re.sub(r'\d:[0-5]\d','',oral_contents)
oral_contents = re.sub(r'(20|21|22|23|[0-1]\d):[0-5]\d','',oral_contents)

# remove '~' for there is not such character in author names or numbers
oral_contents = re.sub(r'~','',oral_contents)

# remove '&amp;'  
oral_contents = re.sub(r'&amp;','',oral_contents)

# first split
splited_oral_contents = re.split(r'\n\n\n',oral_contents)

for splited_oral_content in splited_oral_contents:
	splited_oral_content = splited_oral_content.rstrip()
	
splited_oral_contents[-1] = splited_oral_contents[-1].rstrip()

# second split
further_splited_oral_contents = []
for splited_oral_content in splited_oral_contents:
	further_splited_oral_content = re.split(r'\n\n',splited_oral_content)
	further_splited_oral_contents.append(further_splited_oral_content)

# remove abstract
for further_splited_oral_content in further_splited_oral_contents:
	if len(further_splited_oral_content) == 3:
		# some items does not contain abstract
		del further_splited_oral_content[-1]

# remove title
for further_splited_oral_content in further_splited_oral_contents:
	splited_oral_title = re.split(r'\n',further_splited_oral_content[0])
	further_splited_oral_content[0] = splited_oral_title[0]
	further_splited_oral_content[0].strip()

# remove brackets(twice)
for further_splited_oral_content in further_splited_oral_contents:
	further_splited_oral_content[1] = re.sub(r'\((.*?)\)','&',further_splited_oral_content[1])
for further_splited_oral_content in further_splited_oral_contents:
	further_splited_oral_content[1] = re.sub(r'\((.*?)\)','&',further_splited_oral_content[1])
	
# seperate authors
for further_splited_oral_content in further_splited_oral_contents:
	authors = re.split(r'&|;|,|\band\b',further_splited_oral_content[1])#
	for author in authors:
		if len(author) <= 4:
			authors.remove(author)
	further_splited_oral_content[1] = authors

# remove spaces in author names
for further_splited_oral_content in further_splited_oral_contents:
	further_splited_oral_content[1] = remove_spaces(further_splited_oral_content[1])

## print all
#for further_splited_oral_content in further_splited_oral_contents:
	#for item in further_splited_oral_content:
		#print(item)

# ----------------------------------
# ----------------------------------
# --------output--------------------
# ----------------------------------
# ----------------------------------

# get all authors
author_list = []
for further_splited_content in further_splited_contents:
	# poster authors
	author_list.extend(further_splited_content[1])
for further_splited_oral_content in further_splited_oral_contents:
	# oral authors
	author_list.extend(further_splited_oral_content[1])

# remove duplicate authors and sort alphabetically
author_list = list(set(author_list))
author_list.sort()

# remove non-human-name authors which are too short
for author in author_list:
	if len(author) <= 4:
		author_list.remove(author)

# merge poster and oral lists
further_splited_contents.extend(further_splited_oral_contents)

# search author in merged list bruceforcely, save information formatted [['author name'], [number1, number2, ...]]
authors_numbers = []
author_id = 0
for author in author_list:
	authors_numbers.append([author])
	for further_splited_content in further_splited_contents:
		if author in further_splited_content[1]:
			authors_numbers[author_id].append(further_splited_content[0])
	author_id += 1

# open target written file
with open(output_file_name,'w') as file_output:
	
# fprint all authors with their numbers
	for autnum in authors_numbers:
		file_output.write(autnum[0]+'\n')
		for num in autnum[1:]:
			file_output.write(num+' ')
		file_output.write('\n\n')

