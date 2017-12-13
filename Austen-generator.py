#!/usr/bin/python3
__author__ = 'Alan Au'
__date__   = '2017-12-12'

import random

'''
This is a simple Markov Chain generator to produce a "story" (I use this loosely) based on Pride and Prejudice.

The text has been cleaned up, so that each line of the file contains the text of a single paragraph. To do this, all trailing newlines were stripped, but standalone newlines were left alone. Then all double-newlines were repeatedly replaced with single-newlines. I also removed lines with asterisks.

It uses Python lists to store the "first" words in each sentences, and a hash table to store list of follow-up words for every term in the text. Note that the use of lists means that I get frequency weighting for free. Yay!

I left quotation marks in and will have to deal with them.

I'm going to deal with the "Chapter" headings separately.
'''

pp_dict = {} #to hold follow-up words
pp_first = [] #to hold "first" words

inFile = open("pride_and_prejudice.txt",'r') #here's the training data
outFile = open("pp_output.txt",'w') #here's the resulting file
pp = inFile.readlines()

para_length = []

#load up the hash table
for paragraph in pp:
    words = paragraph.strip().split()
    para_length.append(len(words))
    #go from the first to second-to-last word in the paragraph
    for i in range(len(words)-1):
        current = words[i]
        next = words[i+1]

        #store "first" words
        if i == 0: 
            pp_first.append(current)
        
        #map the current word to its next word(s)
        if current in pp_dict:
            pp_dict[current].append(next)
        else:
            pp_dict[current] = [next]

avg_paragraph = int(float(sum(para_length)/len(para_length)))
#print("The average paragraph contains "+str(avg_paragraph)+" words.") #The average paragraph contains 57 words.
print("Done reading input--let's write some stories!")

#okay, let's write some stories!
fullstory = True
min_sentences = 3 #minimum number of paragraphs in a chapter
min_words = 2
sentences = 0
words = 0

chapters = random.randint(1,61) #canonically, there are 61 chapters in "Pride and Prejudice"
chapter = 1
if fullstory:
    outFile.write('Chapter 1\n') #always at least 1 chapter
else:
    chapters = 1

print("We're going to write a "+str(chapters)+"-chapter story.")

in_quote = False
while chapter <= chapters:
    start = random.sample(pp_first,1)
    output = [start[0]]
    #chapter headings
    if start[0] == "Chapter":
        if chapter == chapters: #stop when we would have gone beyond the last chapter
            break
        if sentences < min_sentences: #make sure chapters are some minimum length
            continue
        output.append(str(chapter))
        chapter += 1
        print("Now writing chapter "+str(chapter))
        sentences = 0
    #everything else
    else:
        sentences += 1
        words = 0
        current = start[0]
        while True:
            if current in pp_dict:
                next = random.sample(pp_dict[current],1)
            elif words < min_words:
                next = random.sample(pp_first,1)
            else:
                break
            output.append(next[0])
            current = next[0]
            words += 1
    outFile.write('\n'+' '.join(output)+'\n')
