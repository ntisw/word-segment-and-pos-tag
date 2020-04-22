import tltk 
from pythainlp.tag import pos_tag_sents
from progress.bar import IncrementalBar
import csv

def read_file(file_name) :
    comments = []
    with open('./data/'+file_name+'.csv', mode='r', encoding='utf-8') as csv_file:
        print(f'Read file {file_name}')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            comments.append(row['th'])
    return comments


def word_segment(comments) : #using tltk word_segment
    results = []
    max = len(comments)
    bar = IncrementalBar('Word segment',max = max ,suffix='%(percent)d%%')
    for row in comments:
        
        comment = tltk.nlp.word_segment(row)
        
        comment = comment.replace(">",">|")
        arr = comment.split('|')
        sentences = []
        sentence = []
        for word in arr : 
            
            if(word.find('<s/>')!= -1) :
                #sentence.append(word)
                sentences.append(sentence)
                sentence = []
            else :
                sentence.append(word)
        
        bar.next()
        results.append(sentences)
    bar.finish()

    return results

def word_postag(comments) :
    results = []

    max = len(comments)
    print('function word_postag')

    for sentences in comments :
        pos_tag = pos_tag_sents(sentences, corpus='pud')
        results.append(pos_tag)

    return results

def write_file(path_file,field,rows) : 
    # writing to csv file  
    print(f"write file {path_file}",end = " ")

    with open(path_file, 'w',newline='',encoding='utf-8') as csvfile:  
        # creating a csv writer object  
        csvwriter = csv.writer(csvfile)  
        # writing the fields  
        csvwriter.writerow(field)             
        for row in rows :
            # writing the data rows  
            csvwriter.writerow(row) 
 

def write_file_dict(filename,result):
    print(f"write file ./result/result_{filename}",end = " ")
 
    with open(f'./result/result_{filename}.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [filename]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result : 
            writer.writerow({filename:row})


def merge_files_result():
    print(f"Starting... merge files ./result/result_v1",end = " ")
    files_name = ["patong_google","promthep_google","wat_google",\
        "patong_trip","promthep_trip","wat_trip"]
    results = []
    
    for file_name in files_name : 
        result = read_result_file(file_name)
        results.append(result)

    with open(f'./result/result_v1.csv', mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=files_name)
        writer.writeheader()
        i=0
        while i < len(results[0]) :
            writer.writerow({files_name[0]:results[0][i],\
                files_name[1]:results[1][i],files_name[2]:results[2][i],\
                files_name[3]:results[3][i],files_name[4]:results[4][i],\
                files_name[5]:results[5][i]})
            i+=1

def read_result_file(file_name) : 
    result = []    

    with open('./result/result_'+file_name+'.csv', mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            result.append(row[file_name])
    max = len(result)
    return result

def main () :
    files_name= ["patong_google","promthep_google","wat_google"\
        ,"patong_trip","promthep_trip","wat_trip"]
    for file_name in files_name :
        comments = read_file(file_name)
        comments = word_segment(comments)
        result = word_postag(comments)
        write_file_dict(file_name,result)
    merge_files_result()

main()
