SentenceParser
==============

this is a sentence parsing program in python, requires the brown corpus to be in same location as the .py file.
And it should work, if each of the txt files from the brown corpus are inside the folder with the .py file.
To first run make the frequency table or just upload the one that I have made, then you do not need the brown corpus.

This sentence parser goes through each word in the brown corpus and creates a frequency or likely hood of the word
occuring with a specific tag. Then the tagger chooses the tag with the highest likely hood of occuring, this is how
the unigram tagger works. I then took the now parsed sentence and ran it through my own implementation of the brill
tagger to fix any errors the unigram tagger made.

This tagger is probabbly 90% accuracte at parsing a sentence perfectly, it is only restricted by words that it does not
know and this can be fixed if I implement a better corpus to make my frequency table from.
