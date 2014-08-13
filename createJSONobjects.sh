export PYTHONPATH=$PYTHONPATH:/usr/local/lib/python2.7/site-packages
rm visualization/tmp/*
rm visualization/json/topics/*
rm visualization/json/documents/*
#Stem words and create key value store for stem and most seen representative.
python visualization/stemDocs.py
#Run Mallet
mallet/bin/mallet import-dir --input visualization/tmp --output topic-input.mallet   --keep-sequence --remove-stopwords
mallet/bin/mallet train-topics --doc-topics-threshold 0.10 --input topic-input.mallet --output-state visualization/lda/topic-state.gz --output-topic-keys visualization/lda/topics.tsv --output-doc-topics visualization/lda/docComp.tsv --topic-word-weights-file visualization/lda/words.tsv --num-topics $1
#Empty tmp directory
#Replace --output-topic-keys output that has stems with representative words.
python visualization/replaceStems.py $1
#Create JSON objects
python visualization/createTopicOverviewJSON.py $1
python visualization/createTopicDetailJSON.py $1
python visualization/createDocDetailJSON.py $1