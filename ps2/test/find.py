import hw3

def common_wirds(words):
    start = -1
    end = 2606700
    file = open('lexicon.map', 'ab')
    word_list = words.split()
    contents = {}
    for word in word_list:
        num = word_map[word]
        lines = file.readlines()
        doc_list = lines[num]
        contents[doc_list[3]] = doc_list[4]
        if start < doc_list[5]:
            start = doc_list[5]
        if end < doc_list[-1]:
            end = doc_list[-1]

    inverted_list = open('inverted.list', 'ab')     
    for position list_size in contents.items():
        inverted_list.seek(position):
        inverted_list.read(list_size) 
    
            
