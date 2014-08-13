import os, glob, numpy, nltk, sys, re
from os.path import basename, splitext
from nltk.stem.snowball import SnowballStemmer

# Key Value Store for stem tokens, used to represent stem words by most
# frequently seen representative word.
stemKVS = []

#Given token and stem token, store counts of tokens into stemKVS like so:
# ['stem', [[token, count],],[token,count],...] 
# where the first element is the max element.
# Disclaimer: Very little thought was put into the making of this data structure.
def insertstemToken(token, stem, occurance):
	flag = 0;
	for i in range(len(stemKVS)):
		if(stem == stemKVS[i][0]):
			flag = 1
			flag2 = 0
			for j in range(len(stemKVS[i][1])):
				if token == stemKVS[i][1][j][0]:
					flag2 = 1
					stemKVS[i][1][j][1] += occurance
					if stemKVS[i][1][0][1] < stemKVS[i][1][j][1]:
						tempArray = stemKVS[i][1][0]
						stemKVS[i][1][0] = stemKVS[i][1][j]
						stemKVS[i][1][j] = stemKVS[i][1][0]
					break
			if 0 == flag2:
				stemKVS[i][1].append([token, 1])
			break
	if 0 == flag:
		stemKVS.append([stem,[[token, 1]]])
	
reload(sys)  
sys.setdefaultencoding('utf8')

stemmer = SnowballStemmer("english")

tokenCountWriter = open("visualization/tokenCounts.csv", 'w')
for file in glob.glob("visualization/corpus/*.txt"):
	docReader = open(file, "r")
	tokens = [word for sent in nltk.sent_tokenize(docReader.read()) for word in nltk.word_tokenize(sent)]
	docReader.close()
	
	tokenCountWriter.write(splitext(basename(file))[0])
	tokenCountWriter.write(',')
	docReader = open(file, "r")
	newContent = docReader.read()
	docReader.close()
	
	tokenCount = 0;
	for token in tokens:
		stemToken = stemmer.stem(token)
		occuranceOfToken = newContent.count(token)
		tokenCount += occuranceOfToken
		insertstemToken(token, stemToken, occuranceOfToken)
		tokenReg = r"\b"+re.escape(token)+r"\b"
		newContent = re.sub(tokenReg, stemToken, newContent)
	tokenCountWriter.write(str(tokenCount))
	tokenCountWriter.write('\n')
	docWriter = open("visualization/tmp/" + basename(file), 'w')
	docWriter.write(newContent)
	docWriter.close()
tokenCountWriter.close()

#Test KSV
#for i in range(len(stemKVS)):
#	rep = ''
#	for j in range(len(stemKVS[i][1])):
#		rep += ('['+stemKVS[i][1][j][0] + ',' + str(stemKVS[i][1][j][1]) + ']')
#	print stemKVS[i][0] + rep
#
#docWriter = open("visualization/stemreps.csv", 'w')
#for i in range(len(stemKVS)):
#	docWriter.write(stemKVS[i][0] + ',' + stemKVS[i][1][0][0] +'\n')
#docWriter.close()

