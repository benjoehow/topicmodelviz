import os, sys, re
from os.path import basename, splitext
import glob

topicNumber = int(sys.argv[1]);
#Array for premade words made in replaceStems.py
wordArray = []
topicsDocs = []
# [[[document, weight][document, weight],...]]
# Where topicsDocs[i] corresponds to topic i
# topicsDocs[i][0] is document with largest weight, this level is sorted by weight
#topicsDocs[i][j][0] is the document basename
#topicsDocs[i][j][1] is the document's weight wrt topic i
for i in range(topicNumber):
	topicsDocs.append([])
order = [0]

documentTokenCount = []

#Maintains sorted array of documents based on weight
def insertDoc(docName, index, weight):
	if(not topicsDocs[index]):
		topicsDocs[index].append([docName, weight, 0])
	else:
		for i in range(len(topicsDocs[index])):
			if float(topicsDocs[index][i][1]) < weight :
				topicsDocs[index].insert(i, [docName,weight,0])
				break
			elif i == len(topicsDocs[index])-1:
				topicsDocs[index].append([docName,weight,0])
				break

tokenCountReader = open('visualization/tokenCounts.csv','r')
for line in tokenCountReader:
	values = re.split(',', line)
	documentTokenCount.append(values)
tokenCountReader.close()

reader = open('visualization/lda/docComp.tsv', 'r')
#Add up all document weights into weight vector.
next(reader)
for line in reader:
	values = re.split('\s', line)
	for i in range(len(values)):
		if line.strip():
			if(i >= 2):
				if i%2==0 and re.match("\d+", values[i]):
					insertDoc(splitext(basename(values[1]))[0], int(values[i]), float(values[i+1]))
reader.close()

for i in range(len(topicsDocs)):
	maxRelevance = 0.0
	for j in range(len(topicsDocs[i])):
		for k in range(len(documentTokenCount)):
			if topicsDocs[i][j][0] == documentTokenCount[k][0]:
				topicsDocs[i][j][2] = float(topicsDocs[i][j][1])*float(documentTokenCount[k][1])
				if (topicsDocs[i][j][2] > maxRelevance):
					maxRelevance = topicsDocs[i][j][2]
				break
	for j in range(len(topicsDocs[i])):
		topicsDocs[i][j][2] = topicsDocs[i][j][2]/maxRelevance
				



for i in range(topicNumber):
	tempMax = topicsDocs[i][0][1];
	for j in range(len(topicsDocs[i])):
		topicsDocs[i][j][1] = float(topicsDocs[i][j][1])/float(tempMax)

#Load premade output for words from replaceStems
reader = open('visualization/wordprevJSONarray.txt','r')
for line in reader:
	values = re.split('\t', line)
	wordArray.append(values[1])
reader.close()

#Write topic overview json file
for j in range(topicNumber):
	jsonWriter = open('visualization/json/topics/topic_' + str(j) + '.json', 'w')
	jsonWriter.write("{\"words\":[")
	jsonWriter.write(wordArray[j].rstrip('\n'))
	jsonWriter.write("],\"documents\":[") 
	for i in range(len(topicsDocs[j])):
		jsonWriter.write("{\"docid\":\"")
		jsonWriter.write(str(topicsDocs[j][i][0]))
		jsonWriter.write("\",\"weight\":" + str(topicsDocs[j][i][1]))
		jsonWriter.write(",\"relev\":" + str(topicsDocs[j][i][2]) + "}")
		if(not i == len(topicsDocs[j])-1):	
			jsonWriter.write(",")
	jsonWriter.write("]}")
	
jsonWriter.close()




			
