#!/usr/bin/python3
__author__ = 'Alan Au'
__date__   = '2017-12-07'

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

#load up the hash table
for paragraph in pp:
    words = paragraph.strip().split()
    #go from the first to second-to-last word in the paragraph
    for i in range(len(words)-1):
        current = words[i]
        next = words[i+1]
        
        #get rid of opening/closing quotation marks because they break my hash lookups
        if current[0] == '“': 
            current = current[1:]
        if current[-1] == '”': 
            current = current[:-1]
        if next[0] == '“': 
            next = next[1:]
        if next[-1] == '”': 
            next = next[:-1]

        #store "first" words
        if i == 0: 
            pp_first.append(current)
        
        #map the current word to its next word(s)
        if current in pp_dict:
            pp_dict[current].append(next)
        else:
            pp_dict[current] = [next]

#okay, let's write some stories!
chapters = random.randint(1,2)
chapter = 0

while chapter <= chapters:
    start = random.sample(pp_first,1)
    output = [start[0]]
    if start == "Chapter":
        output.append[str(chapter)]
    else:
        current = start[0]
        while current[-1] != '.' and current[-1] != '?' and current[-1] != '!':
            try:
                if pp_dict[current]:
                    print(current)
                    next = random.sample(pp_dict[current],1)
                    output.append(next[0])
                    current = next[0]
                else:
                    break
            except 'KeyError':
                continue
    outFile.write(' '.join(output)+'\n')
