#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import collections
import re
import stopwords

# Replace all non-letters with a space
def replaceNonLetters(s):
	# Get all non-letters in the string
	nonLetters = [x for x in s if not x.isalpha()]

	# Replace all non-letters in the string by space
	for char in nonLetters:
		s = s.replace(char," ")
	return s

# Turn all letters into lower case
def toLowerCase(s):
	s = s.lower()
	return s

# Remove common words
def removeCommonWords(wordText,removeList):
	for w in removeList:
		wordText = re.sub('\\b'+w+'\\b','',wordText)
	return wordText

# Lemmalization 
# Form of lemma-list,for example: walk->walks,walking,walked
def lemmatize(wordText,lemmaList):
	for line in lemmaList:
		lemmaAB = line.split("->")
		if len(lemmaAB) > 1:
			lemmaB = lemmaAB[1].split(",")
			for w in lemmaB:
				wordText = re.sub('\\b'+w+'\\b',lemmaAB[0],wordText)
	return wordText

# Get 5000 most common words
def getCommonWords(text):
	strByLine = text.split("\n")
	wordList = [x.split(".")[1] for x in strByLine if x!=""]
	return wordList

# Get lemma-list 
def getLemmaList(text):
	text = text.replace(' ','')
	text = toLowerCase(text)
	lemmaByLine = text.split("\n")
	lemmaList = [x for x in lemmaByLine]
	return lemmaList
	
# Get the specific file content
def getFileContent(file,method):
	with open(file,method,encoding='utf-8') as f:
		content = f.read()
	return content

# Get CET-4 words
def getCET4():
	text = getFileContent("cet-4.txt","r")
	wordList = text.split("\n")
	return wordList
	
def main():
	# Get words to remove and to replace
	print("Loading Words to Remove...")
	commonWordsText = getFileContent("5000_Most_Common_Words.txt","r")
	removeList = getCommonWords(commonWordsText)
	stopWords = stopwords.getStopWords()
	cet4List = getCET4()

	lemmaText = getFileContent("BNC_lemmafile5.txt","r")
	lemmaList = getLemmaList(lemmaText)

	# Get words text and clean it
	print("Loading Words List...")
	myString = getFileContent("ken.txt","r")
	myString = toLowerCase(myString)
	myString = replaceNonLetters(myString)

	print("Lemmalizing...")
	myString = lemmatize(myString,lemmaList)  
	
	print("Removing stopwords...")
	myString = removeCommonWords(myString,removeList)
	myString = removeCommonWords(myString,cet4List)
	myString = removeCommonWords(myString,stopWords)

	print("Counting Frequency...")
	myWordList = myString.split(" ")
	myWordList = [w for w in myWordList if not len(w)<3]
	myWordFreq = collections.Counter(myWordList)

	# Save result
	print("Save to File...")
	with open("myResult10-3.txt","a",encoding='utf-8') as f:
		for key,value in myWordFreq.items():
			# Get rid of which frequency less than one
			if value > 1:
				f.write(key+"\t"+str(value)+"\n")	
	print("Success...")

if __name__ == '__main__':
	main()




