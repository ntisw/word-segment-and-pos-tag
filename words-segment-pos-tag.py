import tltk
import csv
from pythainlp.tag import pos_tag_sents

def word_segment(filename) : #using tltk word_segment
    comments = []
    
    with open('./data/'+filename+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            comment = tltk.nlp.word_segment(row['th'])
            #print(comment)
            comment = comment.replace(">",">|")
            arr = comment.split('|')
            #print(arr)
            sentences = []
            sentence = []
            for word in arr : 
                
                if(word.find('<s/>')!= -1) :
                    #sentence.append(word)
                    sentences.append(sentence)
                    sentence = []
                else :
                    sentence.append(word)
            #print(sentences)
            comments.append(sentences)
    return comments

def word_postag(comments) :
    results = []
    for sentences in comments :
        pos_tag = pos_tag_sents(sentences, corpus='pud')
        #print(pos_tag)
        results.append(pos_tag)
    return results

def write_file(comments,path) : 
    

comments = word_segment('wat_trip')
results = word_postag(comments)
