lexicon = open('lexicon.rpt', 'ab')
pre = ''
global myfile
myfile = open('inverted.list', 'ab')

line = 0
global word_fre
chuck_size = 10

word_fre = ''
words = {}

def print_merge():
    if pre in words:
        word_fre = ''
        n = 0
        for k in words[pre]:
            n += 1
            myfile.write(' ' + str(k))
            word_fre += (' ' + str(words[pre][k]))
            if n % chuck_size == 0:
                myfile.write(word_fre)
                word_fre = ''

for line_str in open('merge.rpt', 'rb'):
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

        lexicon.write(word + ' ' + file_name + ' ' + str(line % 10000 + 1) + '\n')
        
        words[word] = {}
        words[word][id] = 1
        line += 1
        words.pop(pre, None)
        pre = word

print_merge()

#print words
lexicon.close()
myfile.close()
