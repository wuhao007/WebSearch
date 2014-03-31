#!/usr/bin/env python
# Cross-Language Information Retrieval System
# Implements a simple CLIR system on the EUROPARL documents contained in the 
# NLTK corpora.
#
# David Coles (239715), 2010

import codecs
from optparse import OptionParser
import os
import sys

# Import desired corpora
import nltk.corpus.europarl_raw as europarl_raw

from query import BM25
from index import SimpleIndex

def generate_index(corpus, file_obj):
    # The Europarl corpus in NLTK contains approximately 10 days procedings 
    # for each language. To make this interesting for indexing we'll index the 
    # chapters for each day giving us ~80 "documents".
    # http://code.google.com/p/nltk/issues/detail?id=415

    # Index the chapters for all the sessions in the corpus
    index = SimpleIndex()
    for fileid in corpus.fileids():
        chapters = corpus.chapters(fileid)
        for chapterid in range(len(chapters)):
            chapter = chapters[chapterid]
            # Flatten the chapter down to a string for indexing
            text = '\n'.join([' '.join(sentence) for sentence in chapter])

            index.add_document((fileid, chapterid), text)

    index.save(file_obj)
    return index


def do_query(query, indexes, lang):
    # Apply the BM25 model to our index
    index = indexes[lang]
    bm25 = BM25(index)

    # Score all documents
    scores = {}
    for document in index.documents():
        scores[document] = bm25.score(document, query)

    sorted_docs = sorted(scores, key=lambda k: scores[k], reverse=True)

    # Return a list of (score, doc) tuples sorted by score
    return [(scores[doc], lang, doc) for doc in sorted_docs]


def load_dictionary(file_obj):
    """ Loads up a bilingual dictionary from a file-like object
    """
    dictionary = {}

    for line in file_obj:
        try:
            l = line.strip()
            e, fs = l.split(':')
            dictionary[e] = set([f.strip() for f in fs.split(';')])
        except ValueError:
            # Make the reader slightly robust
            print >> sys.stderr, "Could not parse dictionary line: %s"%l

    return dictionary


def query_translation(query, dictionary):
    """ Translates a query using a bilingial dictionary
    """
    translated_query = []

    # Simple unbalanced query
    for term in query:
        translated_query.extend(dictionary.get(term, []))

    return translated_query


def snippet(document, lang):
    fileid, chapter = document
    doc = europarl_raw.__dict__[lang].chapters(fileid)[chapter]

    # TODO: Better snipping algorithm
    return ' '.join(doc[0]) 


SUPPORTED_LANGS = ["english", "french"]

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-i", "--index", action="store_true", dest="index", 
            help="Force regenerate indexes")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        print >> sys.stderr, "Must provide query language as first argument"
        sys.exit()
    elif len(args) <2:
        print >> sys.stderr, "Must provide query on command line"
        sys.exit()

    query_lang = args[0].lower()
    query = args[1:]

    if query_lang not in SUPPORTED_LANGS:
        print >> sys.stderr, "Language '%s' is not supported."%lang
        print >> sys.stderr, "Supported languages: %s"%(
                ', '.join(SUPPORTED_LANGS))
        sys.exit()

    # Load the Indexes for supported languages
    indexes = {}
    for lang in SUPPORTED_LANGS:
        filename = "%s.dat"%lang
        if os.path.exists(filename) and not options.index:
            # Use the cached index
            with open(filename) as f:
                indexes[lang] = SimpleIndex(f)
        else:
            # Generate new index
            print >> sys.stderr, "Generating index for %s"%lang
            with open(filename, 'w') as f:
                corpus = europarl_raw.__dict__[lang]
                indexes[lang] = generate_index(corpus, f)

    # Load dictionaries
    dictionaries = {}
    for lang in SUPPORTED_LANGS:
        if lang != query_lang:
            try:
                filename = "%s-%s.dict"%(query_lang, lang)
                with codecs.open(filename, 'r', 'utf-8') as f:
                    dictionaries[lang] = load_dictionary(f)
            except IOError:
                print >> sys.stderr, (
                        "Could not find required dictionary: %s"%filename)
                sys.exit(1)

    # Search each language
    results = []
    for lang in SUPPORTED_LANGS:
        if lang == query_lang:
            # Normal IR
            results += do_query(query, indexes, lang)
        else:
            # Cross Language IR
            translated_query = query_translation(query, dictionaries[lang])
            results += do_query(translated_query, indexes, lang)

    # Find top 10 results
    results.sort(reverse=True)
    top = results[:10]
    for i in range(len(top)):
        score, lang, document = top[i]
        fileid, chapter = document

        # Stop if score hits 0
        if score <= 0:
            break

        print "%d - %s:%d (Score: %.2f)"%(i+1, fileid, chapter, score)
        print snippet(document, lang)
        print
