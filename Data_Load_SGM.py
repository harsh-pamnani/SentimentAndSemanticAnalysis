import re
import csv

# Method for cleaning the body of the article
def clean_body(body):
    body = body.replace("Reuter &#3;", "")
    
    # Removes the redundant white spaces
    body = re.sub(r'\s+', ' ',body)
    
    # Converting the whole document to lowercase letters
    body = body.lower()
    
    # Removing all the stop words from the tweet
    for stop_word in stop_words_list:
        body = re.sub(' '+stop_word+' ', ' ', body)
    
    # Removing the new line characters with space.
    body = re.sub(r'\\n', ' ', body)
    
    # Remove all other special characters except alphabets, digits, space and plus sign
    body = re.sub(r"[^a-zA-Z ]+", '', body)
    
    return body

# Creating a stop words list from words_stop.txt file.
stop_words_file = open('words_stop.txt','r')
stop_words_list = []
for word in stop_words_file:
    stop_words_list.append(word.replace("\n",""))

# Opening the SGM file in read-only mode
file = open("reut2-000.sgm","r")

# Reading all the lines from the file and attaching it in the new string "newfilelines"
newfilelines = ''
for line in file:
	newfilelines += line

# Getting all the articles written inside <BODY> and </BODY> tag
body_texts = re.compile('<BODY>(.*?)</BODY>', re.DOTALL).findall(newfilelines)

# Opening the result file in write where all the articles retrieved from SGM file will be stored
csvFile = open("Reuter_Data_All.csv",'a', newline='')
fieldnames = ['BODY']
csvWriter = csv.DictWriter(csvFile, fieldnames=fieldnames)
#csvWriter.writeheader()

for body in body_texts:
	# Replaceing the string "Reuter\n&#3;" at the end of every body with ""
	body = body.replace(" Reuter\n&#3;", "")
	
	# As I am using CSV file for writing, replacing all the commas with ""
	body = body.replace(",", "")
	
	# Replacing all the new line characters by space
	body = body.replace("\n", " ")
	
	# Clean the body article before writing it to CSV file
	body = clean_body(body)
	
	# Writing the row to CSV file
	body_dict = {'BODY':body}
	csvWriter.writerow(body_dict)