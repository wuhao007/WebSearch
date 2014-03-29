lexicon = open('lexicon.rpt', 'ab')
pre = ''
global myfile
myfile = None
line = 0
global file_name
file_name = ''
words = {}
for line_str in open('merge1.rpt', 'rb'):
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
        if line % 10000 == 0:
            if myfile != None:
                myfile.close()
            file_name = 'merge_' + str(line/10000) + '.map'
            myfile = open(file_name, 'ab')
        if pre in words:
            myfile.write(pre)
            for k in sorted(words[pre].keys()):
                myfile.write('  ' + str(k) + ' ' + str(words[pre][k]))
            myfile.write('\n')

        lexicon.write(word + ' ' + file_name + ' ' + str(line % 10000 + 1) + '\n')
        
        words[word] = {}
        words[word][id] = 1
        line += 1
        words.pop(pre, None)
        pre = word

#print words
lexicon.close()
myfile.close()
