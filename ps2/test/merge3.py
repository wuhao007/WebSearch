lexicon = open('lexicon.rpt', 'ab')
import pickle
words = {}
line = 1
for line_str in open('merge.rpt', 'rb'):
    v = line_str.split()
    word = v[0]
    id = int(v[1])
    if word in words:
        fre = words[word]
        if id in fre:
            fre[id] += 1
        else:
            fre[id] = 1
    else:
        lexicon.write(word + ' ' + str(line) + '\n')
        line += 1
        words[word] = {}
        words[word][id] = 1

with open('inverted.list', 'w') as inverted_list:
    pickle.dump(words, inverted_list)

lexicon.close()
