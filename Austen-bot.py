#!/usr/bin/python3
__author__ = 'Alan Au'
__date__   = '2017-12-12'

import random

'''
This is a simple Markov Chain generator to produce a "story" (I use this loosely) based on Pride and Prejudice.

The text has been cleaned up, so that each line of the file contains the text of a single paragraph. To do this, all trailing newlines were stripped, but standalone newlines were left alone. Then all double-newlines were repeatedly replaced with single-newlines. I also removed lines with asterisks.

It uses Python lists to store the "first" words in each sentences, and a hash table to store list of follow-up words for every term in the text. Note that the use of lists means that I get frequency weighting for free. Yay!

I left quotations in and deal with them differently than exposition text.

I'm going to deal with the "Chapter" headings separately.
'''

pp_dict = {} #to hold follow-up words in general prose
pp_quote = {} #to hold follow-up words within quotations
pp_first = [] #to hold "first" words
pp_title = {} #to hold potential "title" words

inFile = open("pride_and_prejudice.txt", 'r', encoding="utf8") #here's the training data
outFile = open("pp_output.txt", 'w', encoding="utf8") #here's the resulting file
pp = inFile.readlines()

#load up the hash tables
for paragraph in pp:
    words = paragraph.strip().split()
    len_words = len(words)
    if len_words == 0: continue #don't bother indexing empty paragraphs
    in_quote = False
    #go from the first to second-to-last word in the paragraph
    for i in range(len(words)-1):
        current = words[i]
        next = words[i+1]

        if i == 0: pp_first.append(current) #store "first" words
        if current[0].upper() == 'P': 
            title_word = current.upper()
            while title_word[-1] not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                title_word = title_word[:-1]
            if title_word not in pp_title:
                pp_title[title_word] = True
        
        #map the current word to its next word(s)
        if '“' in current: in_quote = True
        if '”' in current: in_quote = False #in case of one-word quotes, this will revert to False
        if in_quote:
            if current in pp_quote: pp_quote[current].append(next)
            else: pp_quote[current] = [next]
        else:
            if current in pp_dict: pp_dict[current].append(next)
            else: pp_dict[current] = [next]
            
#okay, let's write some stories!
fullstory = True #can set this to False if you just want a single paragraph

chapters = random.randint(1,61) #canonically, there are 61 chapters in "Pride and Prejudice"
chapter = 1
if fullstory:
    title_words = random.sample(pp_title.keys(),2)
    title = title_words[0]+" AND "+title_words[1]
    outFile.write(title.upper()+'\n'+"by Austen-bot (https://github.com/AlanAu/Austen-bot)\n")
    outFile.write('\nChapter 1\n')
else:
    chapters = 1

print("Done reading input--let's write a "+str(chapters)+"-chapter story.")

sentences = False
in_quote = False
while chapter <= chapters:
    start = random.sample(pp_first,1)
    if '“' in start[0]: in_quote = True
    if '”' in start[0]: in_quote = False
    output = [start[0]]
    #chapter headings
    if start[0] == "Chapter":
        if not sentences: continue #make sure there's at least 1 sentence in the chapter
        #stop when we would have gone beyond the last chapter
        chapter += 1
        sentences = False
        if chapter > chapters: break
        output.append(str(chapter))
    #everything else
    else:
        sentences = True
        current = start[0]
        while True:
            if in_quote and current in pp_quote:
                next = random.sample(pp_quote[current],1)
            elif current in pp_dict:
                next = random.sample(pp_dict[current],1)
            else:
                if in_quote:
                    in_quote = False
                    output[-1] = output[-1]+'”'
                break
            output.append(next[0])
            current = next[0]
            if '“' in current: in_quote = True
            if '”' in current: in_quote = False
    outFile.write('\n'+' '.join(output)+'\n')
