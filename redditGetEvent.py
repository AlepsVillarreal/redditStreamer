#! usr/bin/env python3
import praw
import pandas as pd
from datetime import datetime
import pprint
from collections import Counter
import re
from credentials import redditPersonalUseID, redditSecretKey, redditAppName, redditUserName, redditPassword
import matplotlib.pyplot as plt
import seaborn as sns

#30 api calls per minute

"""
TODO
1.Refactor in OOP way
2.Clean incoming data from non alphabetical or numerical characters, such as [], #, !, /, etc
3. Stream to a localFile.txt the dataframe of wordCounterDF
4. #In another script, create a program to read the localFile.txt into a dataframe and then use wordcloud library to plot
"""

#Create a praw reddit object
reddit = praw.Reddit(client_id=redditPersonalUseID, 
                     client_secret=redditSecretKey, 
                     user_agent=redditAppName,
                     username=redditUserName,
                     password=redditPassword)

#Subreddits to analyze
sourceData = ['mexico']

#Create a list that holds subreddit objects from sourceData
subrList=[]
for subr in sourceData:
	subrList.append(reddit.subreddit(subr))

#Create dataframe skeletons for for the text itself and another one for the most repeated word and its counter
comment_dict = { "parent_id":[],
              "original":[],
              "body":[],
            }

wordCounterDf = {"word":[],
				"counter":[]
				}

#final amlo mentions DF
#amloMentionsDf = pd.DataFrame(comment_dict)
wordCounterDf = pd.DataFrame(wordCounterDf)
counterDataFrameColumns = ['word', "counter"]

#Create a regex object to look for any mention of amlo
patternToLookFor = re.compile('amlo', re.IGNORECASE)
for comment in subrList[0].stream.comments():
	try:
		#print (comment.body)
		if len(comment.body) > 0:
			if re.search(patternToLookFor, comment.body):
				print('found an amlo')
				#print(comment.body)
				parent_id = str(comment.parent())
				original = reddit.comment(parent_id)
				comment_dict["parent_id"].append(str(comment.parent()))
				comment_dict["original"].append(original)
				comment_dict["body"].append(comment.body)
				comment_df = pd.DataFrame.from_dict(comment_dict)
				#Split the text of message body in different words in a list
				splittedWordsDf = comment_df['body'].str.lower().str.split()
				for word in splittedWordsDf:
					#print (Counter(word))
					#Now to create the dataFrame that holds the count itself
					counterDataFrame = pd.DataFrame.from_dict(Counter(word), orient='index').reset_index()
					counterDataFrame.columns = counterDataFrameColumns
				#print(counterDataFrame)
				
				#Appending to global wordCounterDf
				wordCounterDf.append(counterDataFrame)
				
				#Convert to CSV file
				#wordCounterDf.to_csv(sep=" ")
				print(wordCounterDf.head())

				#print(splittedWordsDf)
				#print(type(splittedWordsDf))
				#print(splittedWordsDf.describe())
				#print(splittedWordsDf)
				#Get the distinct words
				#results = set()
				#print(splittedWordsDf.str.lower().str.split().apply(results.update))
				#splittedWordsDf.str.lower().str.split().apply(results.update)
				#splittedWordsDf['body'].split().apply(results.update)
				#print(results)
				#wordInComment = (comment.body).split(" ")
				#dictOfComment = dict.fromkeys(wordInComment, 0)
				#amloMentions.update(dictOfComment)
				#for i in range(len(wordInComment)):
		#	if "#" not in wordInComment[i]:
		#		amloMentions[wordInComment[i]] += 1
		#		df = pd.DataFrame(amloMentions, index = [0])
		#		print(df.head())
		#		#amloMentionsDf.append(df)
		#		#print(amloMentionsDf.head())
	except praw.exceptions.PRAWException as e:
		print (e)
		pass

#
def tokenize(text):
	try:
		for row in text:
			for i in row:
				if i is not None:
					words = i.lower().split()
					return words
				else:
					return None

	except Exception as e:
		print(e)
		pass

##Create a dataframe from the dictionary
#df = pd.DataFrame(comment_dict)
#print(df.describe())
#print(df.info())
#print(df.head())

#for comment in subrList[0].stream.comments():
#	try:
#		parent_id = str(comment.parent())
#		original = reddit.comment(parent_id)
#		#if 'amlo' in (original.body):
#		#print('Parent: ')
#		#print(original.body)
#		#print('Reply:')
#		#print(comment.body)
#		wordInComment = (comment.body).split(" ")
#		dict_1 = dict.fromkeys(wordInComment, 0)
#		#print(dict_1.items())
#		for i in range(len(wordInComment)):
#			dict_1[wordInComment[i]] = [1]
#
#		wordDict.update(dict_1)
#
#		df = pd.DataFrame.from_dict(wordDict)
#		print(df.head())
#		#print(wordDict.items())
#	except praw.exceptions.PRAWException as e:
#		print (e)
#		pass

#Get the current suscriber amount and how old the subreddit is:
#for subr in subrList:
#	print ("\n\nName of subreddit: {}".format(subr.title))
#	print("Amount of subscribers: {} \nDate of creation: {}".format(subr.subscribers, datetime.utcfromtimestamp(subr.created_utc)))
#	hot_python = subr.top('year',limit=3)
#	print("Best threads are: ")
#	for topic in hot_python:
#		print ("Title is: {} \n and it has a score of: {}".format(topic.title, topic.score))
#		comments = topic.comments.list()
#		for comment in comments:
#			print(20*"-")
#			print('Parent ID: ', comment.parent())
#			print(comment.body)
#			if len(comment.replies) > 0:
#				for reply in comment.replies:
#					print('REPLY:', reply.body)
#					break
#				break
#			break


#Create dict structure to pass to pandas
#subr_dict = { "id":[],
#              "title":[],
#              "num_comments":[],
#              "score":[],
#              "upvote_ratio":[],
#              "date":[],
#              "created_at":[]
#            }
##Pass to pandas dataframe
#for subr in reddit.subreddit('all').top('year',limit=25):
#    subr_dict["id"].append(subr.id)
#    subr_dict["title"].append(subr.title)
#    subr_dict["num_comments"].append(subr.num_comments)
#    subr_dict["score"].append(subr.score)
#    subr_dict["upvote_ratio"] = subr.upvote_ratio
#    subr_dict["date"].append(datetime.utcfromtimestamp(subr.created_utc))
#    subr_dict["created_at"].append(datetime.utcfromtimestamp(subr.created_utc))
#    
##Create a dataframe from the dictionary
#df = pd.DataFrame(subr_dict)
#
#print(df.head())

#for submission in top_subreddit:
#    topics_dict["title"].append(submission.title)
#    topics_dict["score"].append(submission.score)
#    topics_dict["id"].append(submission.id)
#    topics_dict["url"].append(submission.url)
#    topics_dict["comms_num"].append(submission.num_comments)
#    topics_dict["created"].append(submission.created)
#    topics_dict["body"].append(submission.selftext)
#

#Create a dataframe from the dictionary of dictionaries
#topics_data = pd.DataFrame(topics_dict)
#print(topics_data.head())

#Fix the date column
#def get_date(created):
#	return dt.datetime.fromtimestamp(created)

#_timestamp = topics_data["created"].apply(get_date)
#topics_data = topics_data.assign(timestamp = _timestamp)

#rint (topics_data.head())