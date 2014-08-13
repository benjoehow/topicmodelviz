import os, sys, re
from os.path import basename, splitext
import glob

topicNumber = int(sys.argv[1]);
topicWords = ['']*topicNumber
topicsDocs = []
for i in range(topicNumber):
	topicsDocs.append([])
docTopics = []

#Get topic words
reader = open('visualization/lda/topics.tsv', 'r')			
for line in reader:
	values = re.split('\t', line)
	topicWords[int(values[0])] = values[2]		
reader.close()


reader = open('visualization/lda/docComp.tsv', 'r')
#Add up all document weights into weight vector.
next(reader)
for line in reader:
	values = re.split('\s', line)
	writer = open('visualization/json/documents/' + splitext(basename(values[1]))[0] + '.json', 'w')
	docReader = open('visualization/corpus/'+basename(values[1]), 'r')
	
	contentString = ''
	
	writer.write("{\"content\":[\"")
	for docLine in docReader:
		contentString += "<p>" + docLine.rstrip('\n').replace('\"','')
	writer.write(contentString)
	writer.write("\"],\"topics\":[")
	
	docReader.read()
	tempWeights = [];
	tempMax = values[3];
	for i in range(len(values)):
		if line.strip():
			if(i >= 2):
				if i%2==0 and re.match("\d+", values[i]) and re.match("\d+", values[i+1]):
					tempWeights.append([values[i], values[i+1]])
					
	for i in range(len(tempWeights)):
		tempWeights[i][1] = float(tempWeights[i][1])/float(tempMax)
		writer.write("{\"prev\":"+str(tempWeights[i][1])+",\"words\":\""+topicWords[int(tempWeights[i][0])].rstrip('\n')+"\",\"id\":" + tempWeights[i][0] + "}")
		if not i==len(tempWeights)-1:
			writer.write(",")
	writer.write("]}")
							
	writer.close();
reader.close()

					
			