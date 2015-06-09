"""
Eric Knapik
new sentence parser
mk2
"""
import os
import operator
import re

def mkFrequencyTable():
    """
    this reads in all the files in the folder that the code is in
    then will return a dictionary of words and the amount of times
    that those words occured with the POS tag in the txt files
    """
    words = {} # makes the dictionary that will be used to add words...
    ignoreTags = ['*', '--', '@', '#', '%', '^', '&', '-', '+', '=']
    fileNames = os.listdir(".") #this will change per person
    for num in range(0, len(fileNames) - 2): #prevents it from importing .py
        file = fileNames[num]
        str(file)
        #print(file)

        #file = 'ca01.txt'
        for line in open(file):
            line = line.strip()
            wordLst = line.split()
            for curWord in wordLst:
                #print(word)# use a delimeter / to separate words and POS
                taggedWrd = curWord.split('/')
                #print(taggedWrd)
                base = taggedWrd[0] #base word
                tag = taggedWrd[1] #tag of word
                if base == 'AAb':
                    tag = 'nn'
                if base == 'folds':
                    print(base, tag)
                tag = tagConverter(tag)
                if base == 'folds':
                    print(base, tag)
                words = mkDictionary(words, base, tag)
                """
                #print(tag, counter)

                if tag == '.':
                    counter = 0
                elif tag not in ignoreTags:
                    counter += 1
                #wordDict = {} week 9 for more info make dict in dict ->object
                """
    return words


def tagConverter(tag):
    """
    this converts tags so that they are more easily readable and so that
    the tagger will work more effectively
    """
    if '-' in tag or '+' in tag:
        length = len(tag)
        if length == 5:
            tag = tag[:2]
        if length == 6:
            tag = tag[:3]
        if length == 7:
            tag = tag[:4]

    nounLst = ['nn', 'nn$', 'np', 'nps', 'nps$', 'nr', 'ex', 'nns', 'nns$']
    pronounLst = ['pn', 'pn$', 'pp$', 'pp$$','ppl', 'ppls', 
                'ppo', 'pps', 'ppss', 'prp', 'prp$', 'wp$',
                'wpo', 'wps']
    verbLst = ['be', 'bed', 'bez', 'bedz', 'beg', 'bem', 'ben',
                'ber', 'do', 'dod', 'doz', 'hv', 'hvd', 'hvg',
                'hvn', 'vb', 'vbd', 'vbg', 'vbn', 'vbd', 'vbg',
                'vbn', 'vbp', 'vbz', 'doz*', 'hvz']
    adverbLst = ['rb', 'rbr', 'rbt', 'rn', 'rp', 'wrb']
    adjectiveLst = ['jj', 'jjr', 'jjs', 'jjt']
    articleLst = ['at']
    determinerLst = ['dt', 'dti', 'dts', 'dtx', 'abn', 'abx',
                    'ap', 'wdt']
    qualifierLst = ['ql', 'qlp', 'wql', 'abl', 'md', 'md', 'md*']
    
    if tag in nounLst:
        return 'nn'
    elif tag in pronounLst:
        return 'pn'
    elif tag in verbLst:
        return 'vb'
    elif tag in adverbLst:
        return 'advb'
    elif tag in adjectiveLst:
        return 'jj'
    elif tag in articleLst:
        return 'at'
    elif tag in determinerLst:
        return 'dt'
    elif tag in qualifierLst:
        return 'ql'
    else:
        return tag


def mkDictionary(words, base, tag):
    """
    this takes each word and then will state how many times that
    word has been added with the specific part of speech tag
words - dictionary
base - string of the word
tag - string of the part of speech tag
"""
    if base in words: 
        if tag in words[base]:
            words[base][tag] += 1
        else:
            words[base][tag] = 1

    else:
        words[base] = {}
        words[base][tag] = 1

    return words

def mkFrequencyFile(): #this makes a file
    """
    as stated above this makes a file with the word, the part of speech and the likelyhood
    of that word occuring with that part of speech.
    """
    wordsDictionary = mkFrequencyTable()
    file = open('frequencyTable.txt', 'w')
    for words, tagObj in wordsDictionary.items():
        #print(type(positionObj))
        counter = 0
        total = 0
        for tag, objects in tagObj.items():
            total += wordsDictionary[words][tag]
        for tag, objects in tagObj.items():
            frequency = wordsDictionary[words][tag] / total
            if counter < 5:
                frequency = format(frequency, '.2f')
                string = words + ' ' + tag + ' ' + str(frequency) + '\n'
                file.write(string)
                counter += 1
    file.write("parse vb 1.00" + '\n')
    file.write("parser nn 1.00" + '\n')
    file.write("google vb .75" + '\n')
    file.write("google nn .25" + '\n')
    file.write("Google vb .75" + '\n')
    file.write("google nn .75" + '\n')
    """
    print(words + ': ' + tag + "  " +
    str(wordsDictionary[words][tag])) #should be the count of ...
    """
    #print(wordsDictionary)

class TagFrequency():
    __slots__ = ('tag', 'frequency')


def importFrequencyTable():
    """
    this imports the frequency table file that I made
    above and then will take the data and put it into
    a words data dictionary table with the word, tag, and
    likely hood of happening
    returns a dictionary
    """
    file = "frequencyTable.txt"
    frequencyTotal = 0
    counter = 0
    words = {}
    for line in open(file):
        if counter < 3:
            counter += 1
        else:
            line = line.strip()
            line = line.split()

            tagFrequency = TagFrequency()
            tagFrequency.tag = line[1]
            tagFrequency.frequency = float(line[2])
            if line[0] in words:
                words[line[0]].append(tagFrequency)
            else:
                words[line[0]] = []
                words[line[0]].append(tagFrequency)
    return words

class ParsedWord():
    """
    parsed word object and constructor
    """
    __slots__ = ('word', 'tag')

    def __init__(self, word, tag):
        self.word = word
        self.tag = tag

def sentenceParser(sentence, frequencyTable):
    """
    this will go though each word in the sentence wich is passed in
    then it will compare each word to that in the frequencyTable and
    see if it is there. If it is then it will pick the highest % of 
    occurance of that word. and assign a tag to the word
    if the word isnt in the frequencyTable then the word's tag is nn
    for noun
    """
    sentence = fixContractions(sentence, frequencyTable)
    sentence = sentence.strip()
    sentence = sentence.split()
    sentence[0] = sentence[0].title()
    finishedSentence = []
    tempFrequency = 0
    for word in sentence:
        #print(word)
        tag = 'nn'
        if word in frequencyTable:
            tempFrequency = 0
            for tagObject in frequencyTable[word]:
                #print(tagObject.frequency)
                if tagObject.frequency > tempFrequency:
                    tempFrequency = tagObject.frequency
                    tag = tagObject.tag
                    #print(word, " ", tag)
            #tag = frequencyTable[word][0].tag #not sure how to get largest tag
        parsedWord = ParsedWord(word, tag)
        #print(parsedWord.word)
        finishedSentence.append(parsedWord)

    finishedSentence = finalRuleCheck(finishedSentence, frequencyTable)
    for word in finishedSentence:
        print(word.word, ": ", word.tag, "   ", sep='', end = '')

def finalRuleCheck(sentenceLst, freqTable):
    """
    this is the final rule check similar to the Brill tagger this
    will go through and try to improve my tagged words to make
    sure that they are tagged correctly
    returns the sentence list that it is passed in
    """
    sentLength = len(sentenceLst)
    prevTag = ""
    prevWord = ""
    for i in range(0,sentLength):
        word = sentenceLst[i].word
        tag = sentenceLst[i].tag

        if prevTag == 'to' and tag == 'nn':
            if canBeTag(word, 'vb', freqTable):
                sentenceLst[i].tag = 'vb'

        if prevWord == 'would' and tag == 'nn':
            if canBeTag(word, 'vb', freqTable):
                sentenceLst[i].tag = 'vb'

        if prevTag == '*' and tag == 'nn':
            if canBeTag(word, 'vb', freqTable):
                sentenceLst[i].tag = 'vb'

        if (tag == prevTag or prevTag == 'pn') and tag == 'nn':
            if canBeTag(word, 'vb', freqTable):
                sentenceLst[i].tag = 'vb'

        if (tag == prevTag or prevTag == 'vb') and tag == 'vb':
            #if canBeTag(word, 'vb', freqTable):
            sentenceLst[i].tag = 'nn'

        prevTag = tag
        prevWord = word

    return sentenceLst


def canBeTag(word, isTag, freqTable):
    """
    this takes in a word, a tag to check for and the table to look in
    this goes through the table then will check if the word is in the table
    if word in table it checks if the word has that tag available to itself
    if it does then it will return True
    else return false
    """
    if word in freqTable:
        for tagObject in freqTable[word]:
            if isTag == tagObject.tag:
                return True
    return False

def fixContractions(sentence, freqTable):
    """
    this uses the .replace to look for common contractions and then
    will change that word in the sentence to be the actual words because
    the parser does not look at contractions.
    returns the changed sentence
    """
    sentence = sentence.replace("ain't", "are not")
    sentence = sentence.replace("won't", "will not")
    sentence = sentence.replace("can't", "cannot")
    sentence = sentence.replace("n't", " not")
    sentence = sentence.replace("'re", " are")
    sentence = sentence.replace("'m", " am")
    sentence = sentence.replace("'ll", " will")
    sentence = sentence.replace("'ve", " have")
    return sentence

def main():
    print("Enter your choice: ")
    print("1. Make a new frequency table file")
    print("2. Use the existing frequency table file")
    choice = int(input())
    """
    I have commented out the make frequency file because you need to first download the brown corpus .txt files
    this is easier if you use import nltk.corpus.brown(). I just have not implemented it with this functionallity
    this project was more for understanding how nltk taggs its words and trying to implement my own version of it
    Just use the frequency table file I have here and have it in the same directory as the .py
    """

    if choice == 1:
        pass #mkFrequencyFile()
    elif choice == 2:
        table = importFrequencyTable()
        print( canBeTag("notice", "nn", table) )
        sentence = None
        while sentence != "":
            sentence = str(input("Enter the sentence to parse: "))
            if sentence != "":
        	    sentence = re.sub("([!,.:-_;?()])", r" \1", sentence) #regular expressions
        	    #print(sentence)
        	    sentenceParser(sentence, table)
        	    print()
        	    input()
        	    os.system('clear')
    else:
   	    pass





main()




"""
impliment making new corpus from imput
    ask if you want committed then commit
investigate smells and like, influence
//nouns after 'to' are verbs
verbs after 'the' are nouns 
nouns ending in al is an adjective
//impliment nouns after would are verbs
//nouns after not (*) are verbs if they can be
//noun noun check second noun if can be verb -> change second to verb (pn noun -> pn vb)
nieve bays


if __name__ == "__main__":
    do things

help:
    nn (noun)  vb(verb) 

GITHuB

nieve bays after brill tagger rules.
    to look at the words around contractions (we'd)
    give control sentences and it learns
    find words used with eachother, and then guesses the solution.
    

error check input:
    ^A^A^A^A^AA




use unigram tagger then run through brill tagger rule set

class Object():
	__slots__ = ('POS', 'count')

frequency = Object()
frequency.POS = 'noun'
frequency.count = 1
word['cat'] = {}
word['cat'][2] = frequency
 # the second dictionary is the position in the sentence
print(word['cat'][2].POS)
print('it' in word) # should be false
print(word.keys())
print(word.values())


word: POS  word: POS
"""
