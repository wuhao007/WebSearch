#!/usr/bin/env python
# Simple document indexer
# David Coles (239715), 2010

import collections
import cPickle as pickle
import math

default_tokenizer = lambda string: string.split()
default_normalizer = lambda string: string.lower()


class SimpleIndex(object):
    """ A simple document indexer that creates a reverse index of terms to 
    their original documents.
    """

    def __init__(self, index_file=None, tokenizer=default_tokenizer,
            normalizer=default_normalizer):

        if index_file:
            # Load index from file
            self.load(index_file)
        else:
            # Create document index
            self._N = 0
            self._length = {}
            self._index = collections.defaultdict(set)
            self._tf = collections.defaultdict(int)
            self._df = collections.defaultdict(int)

        self.tokenizer = tokenizer
        self.normalizer = normalizer

    def save(self, file_obj):
        """ Saves an index to a file-like object
        """
        data = {'N': self._N,
                'length': self._length,
                'index': self._index,
                'tf': self._tf,
                'df': self._df,
                }
        pickle.dump(data, file_obj)

    def load(self, file_obj):
        """ Loads an index from a file-like object
        """
        # Get all the values first (incase pickle is corrupt)
        data = pickle.load(file_obj)
        N = data['N']
        length = data['length']
        index = data['index']
        tf = data['tf']
        df = data['df']

        # Set the object instance variables
        self._N = N
        self._length = length
        self._index = index
        self._tf = tf
        self._df = df

    def documents(self):
        """ Returns a list of all documents indexed
        """
        return self._length.keys()

    def add_document(self, document_id, text):
        """ Adds a document to the index
        """
        # Add one to the total document count
        self._N += 1

        # Track the length of each document
        self._length[document_id] = len(text)

        # Tokenize
        tokens = self.tokenizer(text)

        # Index normalized versions
        for term in tokens:
            self._index[self.normalizer(term)].add(document_id)

            # Only increment DF once for each unique term in a document
            if (document_id, term) not in self._tf:
                self._df[term] += 1
            self._tf[(document_id, term)] += 1

    def N(self):
        """ The total number of documents indexed
        """
        return self._N

    def term_freq(self, term, document_id):
        """ The number of times a term appears in a specific document
        """
        return self._tf.get((document_id, self.normalizer(term)), 0)

    def doc_freq(self, term):
        """ The number of documents a term appears in
        """
        return self._df.get(self.normalizer(term), 0)

    def length(self, document_id):
        """ Returns the length of a document
        """
        return self._length[document_id]

    def avg_length(self):
        """ Calculates the average length of all the indexed documents
        """
        return float(sum(self._length.values())) / len(self._length)

    def __contains__(self, term):
        return self.normalizer(term) in self._index

    def __getitem__(self, term):
        # Use get so we don't mutate index
        return self._index.get(self.normalizer(term), set())

    def __repr__(self):
        return "<SimpleIndex of %d terms in %d documents>"%(
                len(self._index), self._N)



if __name__ == "__main__":
    # Import desired corpora
    from nltk.corpus.europarl_raw import english, french

    # The Europarl corpus in NLTK contains approximately 10 days procedings 
    # for each language. To make this interesting for indexing we'll index the 
    # chapters for each day giving us ~80 "documents".
    # http://code.google.com/p/nltk/issues/detail?id=415

    # Create an index of the French corpus
    index = SimpleIndex()
    corpus = french

    # Index the chapters for all the sessions in the corpus
    for fileid in corpus.fileids():
        chapters = corpus.chapters(fileid)
        for chapterid in range(len(chapters)):
            chapter = chapters[chapterid]
            # Flatten the chapter down to a string for indexing
            text = '\n'.join([' '.join(sentence) for sentence in chapter])

            index.add_document((fileid, chapterid), text)

    # Save the index
    with open('french.dat', 'w') as f:
        index.save(f)

