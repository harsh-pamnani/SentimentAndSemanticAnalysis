import csv
import re
import math

# Creating a stop words list from words_stop.txt file.
stop_words_file = open('words_stop.txt','r')
stop_words_list = []
for word in stop_words_file:
    stop_words_list.append(word.replace("\n",""))

# Reading the CSV file on which the semantic analysis needs to be performed
csv_reader = csv.reader(open('Document_Reuters_Data_All.csv','r'))
query = "canada"

# Storing all the documents in "documents" list. And all the unique words in "all_words" list
documents = []
all_words = []
for document in csv_reader:
    if(len(document) != 0):
        document = document[0]
		# Cleaning the document before appending it in the documents list
        documents.append(document)
        splitted_document = document.split(" ")
        for word in splitted_document:
            if word not in all_words:
                all_words.append(word)

# Opening the result file
file = open("answer.txt","w") 	

# Sorting all the words alphabetically
all_words = sorted(all_words)
print("Total documents count: ",str(len(documents)))
print("Total words count: ",str(len(all_words)))
file.write("Total documents count: "+str(len(documents))+"\n")
file.write("Total words count: "+str(len(all_words))+"\n\n")
print()

# Creating list for TF matrix
tf_matrix = []

# If the document has multiple query words in it, storing it in a new list "document_with_multiple_words"
document_with_multiple_words = []
for document in documents:
    splited_document = document.split(" ")
    row = []
    for word in all_words:
        temp_word_count = document.count(word)
        if(temp_word_count>1 and word==query):
            document_with_multiple_words.append("D"+str(documents.index(document)+1))
        row.append(temp_word_count)
    tf_matrix.append(row)

# Creaing a matrix for storing IDF values of all the words
word_idf_values = []
length_tf_matrix = len(tf_matrix)
word_counts = []
for word in all_words:
    word_count = 0
    for document in documents:
        if word in document.split(" "):
            word_count += 1
    word_counts.append(1/word_count)
    word_idf_values.append(math.log( (length_tf_matrix/word_count), 2))

# Creating a matrix for TF-IDF
tf_idf_matrix = []
for row in tf_matrix:
    new_row = []
    for i in range (0, len(row)):
        new_row.append(row[i]*word_idf_values[i])
    tf_idf_matrix.append(new_row)

# Splitting the given query
query_words = query.split(" ")
final_query_matrix = []

# Finding the query word in all words and putting calculated values and 0 accordingly
for word in all_words:
    if(word in query_words):
        index = all_words.index(word)
        answer = word_counts[index] * query.count(word) * word_idf_values[index]
        final_query_matrix.append(answer)
    else:
        final_query_matrix.append(0)

# Stroring all the documents in "document_distances" list
document_distances = []
for tf_idf_row in tf_idf_matrix:
    sum = 0
    for element in tf_idf_row:
        sum += element**2
	
	# Finding the root of the sum to find distance
    distance = sum**0.5
    document_distances.append(distance)

# Finding the query distance
query_sum = 0
for query_element in final_query_matrix:
    query_sum += query_element**2
query_distance = query_sum**0.5

# Creaing list for storing all the 
cosine_similarities = []
matching_documents_indexs = []
for i in range (0,len(documents)):
    numerator = 0
    for j in range (0, len(all_words)):
        numerator += (tf_idf_matrix[i][j]*final_query_matrix[j])
    denominator = document_distances[i] * query_distance
	
	# Appending -1 to the cosine_similarities matrix if the document is completely irrelevant
    if(denominator==0):
        cosine_similarities.append(-1)
    else:
        answer = numerator/denominator
        if(answer!=0.0):
            matching_documents_indexs.append(i)
        cosine_similarities.append(answer)

# Sorting all the cosine_similarities in reverse order to find the ranking of the documents
sorted_cosine_similarities = sorted(cosine_similarities, reverse = True)
document_list_rank_wise = []
for element in sorted_cosine_similarities:
    # If the element is 0.0 or -1, it means that all the matching documents are completed
	if(element==0.0 or element==-1):
		break
	document_list_rank_wise.append("D"+str(cosine_similarities.index(element)+1))


# Printing TF matrix and writing it to output file
print("TF matrix")
print(tf_matrix)
file.write("TF matrix\n")
file.write(str(tf_matrix))
file.write("\n")
print()

# Printing TF-IDF matrix and writing it to output file
print("TF IDF matrix")
print(tf_idf_matrix)
file.write("TF IDF matrix\n")
file.write(str(tf_idf_matrix))
file.write("\n")
print()

# Printing Query matrix and writing it to output file
print("Query matrix")
print(final_query_matrix)
file.write("Query matrix\n")
file.write(str(final_query_matrix))
file.write("\n")
print()

# Printing document distances and writing it to output file
print("Document distances")
print(document_distances)
file.write("Document distances\n")
file.write(str(document_distances))
file.write("\n")
print()

# Printing Query distance and writing it to output file
print("Query distance")
print(query_distance)
file.write("Query distance\n")
file.write(str(query_distance))
file.write("\n")
print()

# Printing Cosine similarities and writing it to output file
print("Cosine similarities")
print(cosine_similarities)
file.write("Cosine similarities\n")
file.write(str(cosine_similarities))
file.write("\n\n")
print()


# Printing how many total documents matched
print("Total matching documents")
print(len(cosine_similarities)-cosine_similarities.count(0.0)-cosine_similarities.count(-1))
file.write("Total matching documents\n")
file.write(str(len(cosine_similarities)-cosine_similarities.count(0.0)-cosine_similarities.count(-1)))
file.write("\n\n")
print()

# Printing all the matching documents ranking
print("Matching documents ranking")
print(document_list_rank_wise)
file.write("Matching documents ranking\n")
file.write(str(document_list_rank_wise))
file.write("\n\n")
print()


# Printing content of matching documents
print("Content of matching documents:")
file.write("Content of matching documents:\n")
for index in document_list_rank_wise:
    print(documents[int(index[1:])-1])
    file.write(documents[int(index[1:])-1]+"\n")
    break


# Finding all the documents which has "Canada" multiple times out of the top ranked documents
document_with_multiple_words_ranking = []
for element in document_list_rank_wise:
    if element in document_with_multiple_words:
        document_with_multiple_words_ranking.append(element)

# Printing the output of how many documents are present with multiple times "canada" in it
print()
print("Document with multiple query words in it")
print(document_with_multiple_words_ranking)
file.write("Document with multiple query words in it\n")
file.write(str(document_with_multiple_words_ranking))