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
import os

"""
TODO
1.Refactor in OOP way
2.Clean incoming data from non alphabetical or numerical characters, such as [], #, !, /, etc
3. Stream to a localFile.txt the dataframe of wordCounterDF
4. #In another script, create a program to read the localFile.txt into a dataframe and then use wordcloud library to plot
"""
#Only 30 api calls per minute
class streamComments(object):
	def __init__(self, clientID, clientSecret, userAgent, personalUserName, personalPassword):
		self.redditPersonalUseID = clientID
		self.redditSecretKey = clientSecret
		self.redditAppName = userAgent
		self.redditUserName = personalUserName
		self.redditPassword = personalPassword
		self.counterFileName = 'example.csv'


		try:
			#Create a praw reddit object
			reddit = praw.Reddit(client_id=self.redditPersonalUseID, 
								client_secret=self.redditSecretKey, 
								user_agent=self.redditAppName,
								username=self.redditUserName,
								password=self.redditPassword)

			#Subreddits to analyze
			sourceData = ['OnePiece']

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

			###Regex object creation###
			#Create a regex object to look for any mention of amlo
			patternToLookFor = re.compile('hi', re.IGNORECASE)
			
			
			for comment in subrList[0].stream.comments():
				try:
					#print (comment.body)
					if len(comment.body) > 0:
						if re.search(patternToLookFor, comment.body):
							print('found an amlo')
							#Eliminate all non alphanumerical characters from the message 
							re.sub(r'\W+', '', comment.body)
							print(comment.body)
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
								print(counterDataFrame.head())
								#try:
								#	if os.path.exists(self.counterFileName):
								#		with open(self.counterFileName, 'a') as f:
								#			print('Append mode')
								#			counterDataFrame.to_csv(self.counterFileName, header=False,  sep='\t', encoding='utf-8', index=False)
								#	else:
								#		print ('First time mode')
								#		counterDataFrame.to_csv(self.counterFileName, sep='\t', encoding='utf-8', index=False)
								#except IOError as err:
								#	print(err)	
								#except Exception as e:
								#	print(e)							
							#print(counterDataFrame)
							
							#Appending to global wordCounterDf
							#Convert to CSV file
							#wordCounterDf.to_csv(sep=" ")
							#print(wordCounterDf.head())
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
					return 1

		except praw.exceptions.PRAWException as e:
			print(e)
			return 1
	
#Start of the program
if __name__ == '__main__':
	streamComments(redditPersonalUseID, redditSecretKey, redditAppName, redditUserName, redditPassword)