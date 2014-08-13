#DEPRECATED: File became too complex to maintain...
import os, sys, re
from os.path import basename, splitext
import glob

topicNumber = 7;
topicWords = ['']*topicNumber
weights = [0.0]*topicNumber
finWeights = [0.0]*topicNumber
topicsDocs = []
for i in range(topicNumber):
	topicsDocs.append([])
docTopics = []
order = [0]

def insertDoc(docName, index, weight):
	if(not topicsDocs[index]):
		topicsDocs[index].append([docName, weight])
	else:
		for i in range(len(topicsDocs[index])):
			if float(topicsDocs[index][i][1]) < weight :
				topicsDocs[index].insert(i, [docName,weight])
				break
			elif i == len(topicsDocs[index])-1:
				topicsDocs[index].append([docName,weight])
				break

#Get topic words
reader = open('lda/topics.tsv', 'r')			
for line in reader:
	values = re.split('\t', line)
	topicWords[int(values[0])] = values[2]		
reader.close()


reader = open('lda/docComp.tsv', 'r')
#Add up all document weights into weight vector.
next(reader)
for line in reader:
	values = re.split('\s', line)
	writer = open('json/documents/' + splitext(basename(values[1]))[0] + '.json', 'w')
	docReader = open('corpus/'+basename(values[1]), 'r')
	
	writer.write("{\"content\":[")
	contentHolder = []
	for docLine in docReader:
		contentHolder.append(docLine.rstrip('\n'))
	for i in range(len(contentHolder)):
		writer.write("\"")
		writer.write(contentHolder[i])
		writer.write("\"")
		if not i==len(contentHolder)-1:
			writer.write(",")
	writer.write("],\"topics\":[")
	
	docReader.read()
	tempWeights = [];
	tempMax = values[3];
	for i in range(len(values)):
		if line.strip():
			if(i >= 2):
				if i%2==1 and re.match("\d+", values[i]):
					if values[i] > max:
						tempMax = values[3]
					weights[int(values[i-1])] += float(values[i])
				elif re.match("\d+", values[i]) and re.match("\d+", values[i+1]):
					insertDoc(splitext(basename(values[1]))[0], int(values[i]), float(values[i+1]))
					tempWeights.append([topicWords[int(values[i])], values[i+1]])
					
	for i in range(len(tempWeights)):
		tempWeights[i][1] = float(tempWeights[i][1])/float(tempMax)
		writer.write("{\"prev\":"+str(tempWeights[i][1])+",\"words\":\""+tempWeights[i][0].rstrip('\n')+"\"}")
		if not i==len(tempWeights)-1:
			writer.write(",")
	writer.write("]}")
							
	writer.close();
reader.close()

					
					
#Find maximum joint doc weight
max = weights[0]
for i in range(len(weights)):
	if(max < weights[i]):
		max = weights[i]

#Divide each document weight by the max	
for i in range(len(finWeights)):
	finWeights[i] = weights[i]/max
	#Determine order of documents, basically insertion sort
	if(i > 0):
		for j in range(len(order)):
			if finWeights[i] >= finWeights[int(order[j])]:
				order.insert(j, i)
				break
			elif j == len(order)-1:
				order.append(i)
				break
				
				
#Write topic overview json file
jsonWriter = open('json/topics.json', 'w')
jsonWriter.write("{\"topics\":[")
for i in range(len(topicWords)):
	jsonWriter.write("{\"id\":")
	jsonWriter.write(str(i))
	jsonWriter.write(",\"prev\":")
	jsonWriter.write(str(finWeights[int(order[i])]))
	jsonWriter.write(",\"words\":\"")
	jsonWriter.write(topicWords[i].rstrip('\n') + "\"")
	jsonWriter.write("}")
	if(i < len(order)-1):
		jsonWriter.write(",")
jsonWriter.write("]}")

jsonWriter.close()

#Write topic overview json file
for j in range(len(weights)):
	jsonWriter = open('json/topics/topic_' + str(j) + '.json', 'w')

	jsonWriter.write("{\"words\":[\"")
	jsonWriter.write(topicWords[j].rstrip('\n'))
	jsonWriter.write("\"],\"documents\":[") 
	for i in range(len(topicsDocs[j])):
		jsonWriter.write("\"{\"docid\":")
		jsonWriter.write(str(topicsDocs[j][i][0]))
		jsonWriter.write("\",\"weight\":" + str(topicsDocs[j][i][1]) + "}")
		if(not i == len(topicsDocs[j])-1):	
			jsonWriter.write(",")
	jsonWriter.write("\"]}")
	
jsonWriter.close()