import re, sys

topicNumber = int(sys.argv[1]);
stemrepKVS = []
topicStore = []
wordArray = []
for i in range(topicNumber):
	wordArray.append([])

stemrepReader = open("visualization/stemreps.csv",'r')

mallettopicReader = open("visualization/lda/topics.tsv",'r')

#Populate Stem, Representative key value store
for line in stemrepReader:
	stemrepArray = re.split(",",line)
	stemrepKVS.append(stemrepArray)
stemrepReader.close()
	
	
#Replace stems with representative in the topic output file
for line in mallettopicReader:
	values = re.split('\t', line)
	#Ugliest Hack Part 1: Put words into word Array
	words = re.split('\s+', values[2])
	for j in range(len(words)):
		wordArray[int(values[0])].append([words[j], 0.0])
	#Iterate through the KVS, replacing words as they appear.
	for i in range(len(stemrepKVS)):
		if len(stemrepKVS[i])==2:
			stemReg = r"\b"+re.escape(stemrepKVS[i][0])+r"\b"
			values[2] = re.sub(stemReg, stemrepKVS[i][1], values[2])
	topicStore.append(values)
		
mallettopicWriter = open("visualization/lda/topics.tsv", 'w')
for i in range(len(topicStore)):
	topicStore[i][2] = re.sub(r'\n', '', topicStore[i][2])
	mallettopicWriter.write(topicStore[i][0] + '\t' + topicStore[i][1] + '\t' + topicStore[i][2] + '\n')
mallettopicWriter.close()
		
wordPrevReader = open('visualization/lda/words.tsv', 'r')
for line in wordPrevReader:
	values = re.split('\t', line)
	for i in range(len(wordArray[0])):
		if values[1] == wordArray[int(values[0])][i][0]:
			wordArray[int(values[0])][i][1] = float(values[2])

for i in range(len(wordArray)):
	maxWordValue = wordArray[i][0][1]
	for j in range(len(wordArray[i])):
		wordArray[i][j][1] = wordArray[i][j][1]/maxWordValue
		
#Ugliest Hack Part 2: Replace stems AGAIN with representative
for i in range(len(stemrepKVS)):
	for k in range(len(wordArray)):
		for j in range(len(wordArray[k])):
			if wordArray[k][j][0] == stemrepKVS[i][0]:
				wordArray[k][j][0] = stemrepKVS[i][1]
wordPrevReader.close()

wordPrevWriter = open('visualization/wordprevJSONarray.txt', 'w')
for k in range(len(wordArray)):
	wordPrevWriter.write(str(k))
	wordPrevWriter.write('\t')
	for j in range(len(wordArray[k])):
		wordPrevWriter.write('{\"word\":\"')
		wordPrevWriter.write(wordArray[k][j][0].rstrip('\n'))
		wordPrevWriter.write('\",\"prev\":')
		wordPrevWriter.write(str(wordArray[k][j][1]))
		wordPrevWriter.write("}")
		if(not j==len(wordArray[k])-1):
			wordPrevWriter.write(",")
	wordPrevWriter.write('\n')
wordPrevWriter.close()
			
