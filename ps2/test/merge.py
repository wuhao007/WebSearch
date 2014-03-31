lexicon = open('lexicon.rpt', 'ab')
frequency = open('frequency.rpt', 'ab')
global pre
global merge
pre = ''
myfile = open('inverted.list', 'ab')

chuck_size = 10
words = {}
words_map = {}

def print_merge():
    if pre in words:
        myfile.write(pre + ' ')
        lexicon.write(pre + ' ')
        frequency.write(pre + ' ')
        start = myfile.tell()
        fre = words[pre]
        for k in sorted(fre.keys()):
            myfile.write(str(k) + ' ')
            frequency.write(str(fre[k]) + ' ')
        myfile.write('\n')
        frequency.write('\n')
        lexicon.write(str(start) + ' ' + str(myfile.tell()) + '\n') 

merge_rpt = open('merge.rpt', 'rb')
line = 0
for line_str in merge_rpt:
    v = line_str.split()
    word = v[0]
    id = int(v[1])
    if word in words:
        fre = words[v[0]]
        if id in fre:
            fre[id] += 1
        else:
            fre[id] = 1
    else:
        print_merge()
        line += 1
        words_map[word] = line
        words[word] = {}
        words[word][id] = 1
        if pre in words: 
            words.pop(pre, None)
        pre = word
print_merge()
import pickle
pickle.dump(words_map, open('words.map', 'wb'))

#print words
lexicon.close()
frequency.close()
myfile.close()
