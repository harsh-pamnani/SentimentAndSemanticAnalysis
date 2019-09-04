import csv
import re

# Reading files for stop-words, positive-words, and negative-words
stop_words_file = open('words_stop.txt','r')
negative_words_file = open('words_negative.txt','r')
positive_words_file = open('words_positive.txt','r')

stop_words_list = []
negative_words_list = []
positive_words_list = []

# Creating a list for stop words.
for word in stop_words_file:
    stop_words_list.append(word.replace("\n",""))

# Creating a list for negative words.
for word in negative_words_file:
    negative_words_list.append(word.replace("\n",""))

# Creating a list for positive words
for word in positive_words_file:
    positive_words_list.append(word.replace("\n",""))

# Function to clean the given input string
# It removed URL, emoticons, special characters and multiple white spaces
def clean_tweet(tweet):
    # Removes the redundant white spaces
    tweet = re.sub(r'\s+', ' ',tweet)
    
    # Removes URL
    tweet = re.sub(r"http\S+", '', tweet)
    
    # Removing "RT:" text which is present at the starting in the tweet if it is a retweet
    if(tweet.startswith('RT ')):
        tweet = re.sub(r"RT ", '', tweet)
    
    # Removes emoticons from the given input string
    tweet = re.sub(r'\\u[A-Za-z0-9]{4}', '', tweet)
    
    # Removing the new line characters with space.
    tweet = re.sub(r'\\n', ' ', tweet)
    
    # Remove all other special characters except alphabets, digits, space and plus sign
    tweet = re.sub(r"[^a-zA-Z0-9 +]+", '', tweet)
    
    # Returning the cleaned tweet
    return tweet

# Function for performing sentiment analysis on tweet
def sentiment_of_tweets(tweet):
    # Cleaning the tweet text before performing sentiment analysis on it
    tweet = clean_tweet(tweet)
    
	# Removing all the stop words from the tweet
    for stop_word in stop_words_list:
        tweet = re.sub(' '+stop_word+' ', ' ', tweet)
	
    # Getting all the words of the tweet in a list
    tweet_words = tweet.split(" ")
    
    # Performing stemming on the tweet
    stemming_list_words = {"gaming":"game", "games":"game", "gamed":"game", "playing":"play", "plays":"play", "playground":"play", "okay":"ok", "k":"ok", "thankfully":"thank", "thanks":"thank", "thankful":"thank", "secularism":"secular", "prayer":"pray", "respected":"respect", "destroyed":"destroy", "emerged":"emerge", "making":"make"}
    suffix_list = ['ing', 'ed', 'ly', 'ies', 'ious', 'es', 'ive', 'ment', 's']
    
    new_tweet = ""
	# Loop for checking if any word appears in the stemming list of words
    for word in tweet_words:
        new_word = word
        if word in stemming_list_words:
            new_word = stemming_list_words[word]
        new_tweet += (new_word + " ")

	# Loop for finding if the word is ending with any suffix then replacing applying substring to that word
    tweet_words = new_tweet.split(" ")
    new_tweet = ""
    for word in tweet_words:
        new_word = word
        for suffix in suffix_list:
            if word.endswith(suffix):
                new_word = word[:-len(suffix)]
                break
        new_tweet += (new_word + " ")

    tweet = new_tweet
	
	# Initializing the positive and negative word counts with 0
    positive_word_count = 0
    negative_word_count = 0
	
    tweet_words = tweet.split(" ")
    
	# If the word is in positive words list then increasing the count for positive words
    for word in positive_words_list:
        if(word in tweet_words):
            positive_word_count = positive_word_count + 1
	
	# If the word is in negative words list then increasing the count for negative words
    for word in negative_words_list:
        if(word in tweet_words):
            negative_word_count = negative_word_count + 1
    
	# Finding the polarity based on the count of positive and negative words
    if (positive_word_count > negative_word_count):
        positivity = positive_word_count / len(tweet_words)
        return "Positive " + str(positivity)
    elif (negative_word_count > positive_word_count):
        negativity = negative_word_count / len(tweet_words)
        return "Negative " + str(negativity*-1)
    else:
        return "Neutral " + str(0)

#open the csv to read the tweets
csv_read_file = open('Tweets.csv','r')
reader = csv.reader(csv_read_file)

# Openign the CSV file for writing output of sentiment analysis
csv_write_file = open('Sentiment_Analysis_Result.csv', 'w', newline='')
fieldnames = ['Tweet', 'Sentiment', 'Polarity']
csv_writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
csv_writer.writeheader()

# Iterating through all the tweets in the file line by line
for line in reader:
    if(len(line) != 0):
        tweet_text = clean_tweet(line[0])
        
        # Calling the function "sentiment_of_tweets" to find the sentiment of tweet
        sentiment_of_tweet = sentiment_of_tweets(tweet_text)
        sentiment = sentiment_of_tweet.split(" ")[0]
        polarity = sentiment_of_tweet.split(" ")[1]
        
        print(tweet_text)
        print(sentiment)
        
        tweet_dict = {'Tweet':tweet_text, 'Sentiment':sentiment, 'Polarity':polarity}
        csv_writer.writerow(tweet_dict)

# Initializing the positive, negative and netral word count for displaying on console
positive_tweet_count = 0
negative_tweet_count = 0
neutral_tweet_count = 0

# Reading the output file created in the above program
new_csv_reader = csv.reader(open('Sentiment_Analysis_Result.csv','r'))

# Reading every tweet form the file and checking whether it is positive, negative, or neutral
for line in new_csv_reader:
    if(line[1]=="Positive"):
        positive_tweet_count = positive_tweet_count + 1
    elif(line[1]=="Negative"):
        negative_tweet_count = negative_tweet_count + 1
    else:
        neutral_tweet_count = neutral_tweet_count + 1

print()
# Prining the output to console
print("Total positive tweets:", str(positive_tweet_count))
print("Total negative tweets:", str(negative_tweet_count))
print("Total neutral tweets:", str(neutral_tweet_count))