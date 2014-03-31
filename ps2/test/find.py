import pickle

words_map = pickle.load(open('words.map', 'rb'))
inverted_list = open('inverted.list', 'rb').readlines()

def common_words(words):
    word_list = words.split()
    contents = []
    for word in word_list:
        num = words_map[word]
        contents += [inverted_list[num-1].split()[1:]] 
    common_list = set(contents[0])
    print common_list
    for content in contents:
        common_list = common_list.intersection(set(content))
    print common_list

common_words("happy new year")
