lexicon = open('lexicon.rpt', 'ab')
global pre
global merge
pre = ''
myfile = open('inverted.list', 'ab')

chuck_size = 10
words = {}

def print_merge():
    if pre in words:
        lexicon.write(pre + ' ')
        start = myfile.tell()
        myfile.write(pre + ' ')
        n = 0
        word_fre = ''
        docs = ''
        fre = words[pre]
        step = ''
        k = ''
        for k in sorted(fre.keys()):
            if n == 0:
                step += (str(k) + ' ')
            n += 1
            myfile.write(str(k) + ' ')
            #myfile.write(bytes(k))
            #myfile.write(bytes(fre[k]))
            word_fre += (str(fre[k]) + ' ')
            if n % chuck_size == 0:
                step += (str(k) + ' ')
                myfile.write(word_fre)
                word_fre = ''
        myfile.write(word_fre)
        myfile.write('\n')
        lexicon.write(str(start) + ' ' + str(myfile.tell()) + ' ' + step + str(k) + ' ')
        lexicon.write('\n')

merge_rpt = open('merge.rpt', 'rb')
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

        words[word] = {}
        words[word][id] = 1
        if pre in words: 
            words.pop(pre, None)
        pre = word
print_merge()

#print words
lexicon.close()
myfile.close()
