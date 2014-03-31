import math

import index

class BM25(object):
    """ Uses a SimpleIndex to score a document using Okapi BM 25.
    """
    def __init__(self, N, ft, fdt, l, avg_l, k1=1.2, b=0.75):
        self.N = N
        self.ft = ft
        self.fdt = fdt
        self.l = l
        self.avg_l = avg_l
        self.k1 = k1
        self.b = b

    def idf_weight(self, term):
        """ Calculates the inverse document frequency weight of a term
        """
        # To make the formula clear, we set up local variables in terms of the 
        # mathematical description
        N = self.N
        ft = self.ft

        return math.log((N - ft + 0.5)/(ft + 0.5))

    def score(self, document_id, query, contents):
        """ Calculates the Okapi BM25 score for a document
        """
        # To make the formula clear, we set up local variables in terms of the 
        # mathematical description
        f = self.index.term_freq
        D = document_id
        k1 = self.k1
        b = self.b
        l = self.index.length(document_id)
        avg_l = self.index.avg_length()

        score = 0
        for term in query:
            idf = self.idf_weight(term)
            s = idf * (fdt * (k1 + 1)) / (fdt + k1 * (1 - b + b*l/avg_l))
            # Ignore negative scored terms (common terms)
            if s > 0.0:
                score += s

        print score
        return score

import pickle

words_map = pickle.load(open('words.map', 'rb'))
inverted_list = open('inverted.list', 'rb').readlines()

def common_words(words):
    query = words.split()
    contents = []
    for word in query:
        num = words_map[word]
        contents += [inverted_list[num-1].split()[1:]]
    common_list = set(contents[0])
    print common_list
    for content in contents:
        common_list = common_list.intersection(set(content))

    # Hard coded query

    # Load index

    # Apply the BM25 model to our index
    bm25 = BM25(len(common_list))

    # Score all documents
    scores = {}
    for document in common_list:
        scores[document] = bm25.score(document, query, contents)

    sorted_docs = sorted(scores, key=lambda k: scores[k], reverse=True)

    print "Query for: " + ' '.join(query)
    for doc in sorted_docs[:10]:
        print "%10.2f: %s"%(scores[doc], doc)
