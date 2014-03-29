pre = ''
myfile = open('merge2.rpt', 'wb')
words = {}
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
        if pre in words:
            for k in sorted(words[pre].keys()):
                myfile.write(pre + ' ' + str(k) + '\n')

        words.pop(pre, None)
        words[word] = {}
        words[word][id] = 1
        pre = word

#print words
myfile.close()
