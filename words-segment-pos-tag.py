import tltk 
from pythainlp.tag import pos_tag_sents
from progress.bar import IncrementalBar
import csv

def read_file(file_name) :
    comments = []
    path_file = f'./data/{file_name}.csv'
    with open(path_file, mode='r', encoding='utf-8') as csv_file:
        print(f'Read file {path_file}')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            comments.append(row['th'])
    return {"file_name":file_name,"comments":comments}


def word_segment(data) : #using tltk word_segment
    results = []
    file_name = data["file_name"]
    comments = data["comments"]
    max = len(comments)
    bar = IncrementalBar(f'Word segment file {file_name}.csv',max = max ,suffix='%(percent)d%% %(elapsed_td)s')
    for row in comments:
        comment = tltk.nlp.word_segment(row)
        comment = comment.replace(">",">|")
        arr = comment.split('|')
        sentences = []
        sentence = []
        for word in arr : 
            if(word.find('<s/>')!= -1) :
                sentences.append(sentence)
                sentence = []
            else :
                sentence.append(word)
        results.append(sentences)
        bar.next()
    bar.finish()
    return results

def word_postag(comments) :
    results = []
    for sentences in comments :
        pos_tag = pos_tag_sents(sentences, corpus='pud')
        results.append(pos_tag)
    print('Word postag by pythai Done!')
    return results

def write_file_dict(filename,result):
    
    path_file = f'./result/result_{filename}.csv'
    with open(path_file, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [filename]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in result : 
            writer.writerow({filename:row})
    print(f"Write Result file {path_file} Done!")


def merge_files_result(files_name):
    results = []
    for file_name in files_name : 
        result = read_result_file(file_name)
        results.append(result)
    path_file = f'./result/merged_results.csv'
    with open(path_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=files_name)
        writer.writeheader()
        i=0
        while i < len(results[0]) :
            writer.writerow({files_name[0]:results[0][i],\
                files_name[1]:results[1][i],files_name[2]:results[2][i],\
                files_name[3]:results[3][i],files_name[4]:results[4][i],\
                files_name[5]:results[5][i]})
            i+=1
    print(f"Merge files to {path_file} Done!")

def read_result_file(file_name) : 
    result = []    
    path_file = f'./result/result_{file_name}.csv'
    with open(path_file, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            result.append(row[file_name])
    print(f'Read file {path_file} Done!')
    return result

def tltk_segment_pythai_postag(file_name) : 
    data = read_file(file_name)
    word_segment_result = word_segment(data)
    word_postag_result = word_postag(word_segment_result)
    write_file_dict(file_name,word_postag_result)

def main () :
    files_name= ["patong_google","promthep_google","wat_google"\
        ,"patong_trip","promthep_trip","wat_trip"]
    for file_name in files_name :
        tltk_segment_pythai_postag(file_name)
    merge_files_result(files_name)

main()
