import time
tic = time.perf_counter() #timer start
import csv
toc = time.perf_counter() #timer stop
print(f"Importing csv in {toc - tic:0.4f} seconds")
tic = time.perf_counter() #timer start
import tltk 
toc = time.perf_counter() #timer stop
print(f"Importing tltk in {toc - tic:0.4f} seconds")
tic = time.perf_counter() #timer start
from pythainlp.tag import pos_tag_sents
toc = time.perf_counter() #timer stop
print(f"Importing pos_tag_sents in {toc - tic:0.4f} seconds")

def read_file(file_name) :
    comments = []    
    tic = time.perf_counter() #timer start

    with open('./data/'+file_name+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            comments.append(row['th'])

    toc = time.perf_counter() #timer stop
    max = len(comments)
    print(f"read {max} comments at {file_name}.csv in {toc - tic:0.4f} seconds")
    

    return comments

def word_segment(comments) : #using tltk word_segment
    results = []
    i=1 
    max = len(comments)
    tic = time.perf_counter() #timer start
    print(f'functions word segment :')
    tic_ = time.perf_counter() #timer start
    word_count = 0
    for row in comments:
        
        comment = tltk.nlp.word_segment(row)
        
        comment = comment.replace(">",">|")
        arr = comment.split('|')
        sentences = []
        sentence = []
        word_count += len(arr)
        for word in arr : 
            
            if(word.find('<s/>')!= -1) :
                #sentence.append(word)
                sentences.append(sentence)
                sentence = []
            else :
                sentence.append(word)
        results.append(sentences)
        #show percent
        percent = i/max*100
        if percent%10 == 0 :
            toc_ = time.perf_counter() #timer stop
            print (f'{percent}% time {toc_ - tic_:0.4f} seconds per {word_count} words.')
            word_count = 0
            if percent != 100 :
                tic_ = time.perf_counter() #timer start
            
        i+=1

    toc = time.perf_counter() #timer stop
    print(f"Done! {(i-1)} comments in {toc - tic:0.4f} seconds")
    return results

def word_postag(comments) :
    results = []
    i = 1
    max = len(comments)
    print('function word_postag')
    tic = time.perf_counter() #timer start
    tic_ = time.perf_counter() #timer start
    for sentences in comments :
        pos_tag = pos_tag_sents(sentences, corpus='pud')
        results.append(pos_tag)
        #show percent
        percent = i/max*100
        if percent%10 == 0 :
            toc_ = time.perf_counter() #timer stop
            print (f'{percent}%  {toc_ - tic_:0.4f} seconds')
            
            if percent != 100 :
                tic_ = time.perf_counter() #timer start
        i+=1
    toc = time.perf_counter() #timer stop
    print(f"Done! {(i-1)} comments in {toc - tic:0.4f} seconds")
    return results

def write_file(path_file,field,rows) : 
    # writing to csv file  
    print(f"write file {path_file}",end = " ")
    tic = time.perf_counter() #timer start
    with open(path_file, 'w',newline='',encoding='utf-8') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        # writing the fields  
        csvwriter.writerow(field)             
        for row in rows :
            # writing the data rows  
            csvwriter.writerow(row) 
    toc = time.perf_counter() #timer stop
    print(f" in  {toc - tic:0.4f} seconds")

def write_file_dict(filename,result):
    print(f"write file ./result/result_{filename}",end = " ")
    tic = time.perf_counter() #timer start
    with open(f'./result/result_{filename}.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [filename]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result : 
            writer.writerow({filename:row})
    toc = time.perf_counter() #timer stop
    print(f" in  {toc - tic:0.4f} seconds")
def main () :

    files_name= ["patong_google","promthep_google","wat_google"\
        ,"patong_trip","promthep_trip","wat_trip"]
    tic = time.perf_counter() #timer start
    for file_name in files_name :
        comments = read_file(file_name)
        comments = word_segment(comments)
        result = word_postag(comments)
        #write_file(f"./result/result_{file_name}.csv",file_name,result)
        write_file_dict(file_name,result)
    toc = time.perf_counter() #timer stop
    print(f"Success! Elapsed time: {toc - tic:0.4f} seconds")

main()