import os, sys, re
from os.path import basename, splitext
import glob

topicNumber = int(sys.argv[1]);
topicWords = ['']*topicNumber
weights = [0.0]*topicNumber
finWeights = [0.0]*topicNumber
order = [0]

#Get topic words
reader = open('visualization/lda/topics.tsv', 'r')			
for line in reader:
	values = re.split('\t', line.rstrip())
	topicWords[int(values[0])] = values[2]		
reader.close()


#Add up all document weights into weight vector.
reader = open('visualization/lda/docComp.tsv', 'r')
next(reader)
for line in reader:
	values = re.split('\s', line)
	tempWeights = [];
	tempMax = values[3];
	for i in range(len(values)):
		if line.strip():
			if(i >= 2):
				if i%2==1 and re.match("\d+", values[i]):
					weights[int(values[i-1])] += float(values[i])
					
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
jsonWriter = open('visualization/json/topics.json', 'w')
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