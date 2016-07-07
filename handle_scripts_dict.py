#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pickle
import nltk
from nltk.corpus import stopwords
import string
import re


def word_has_alphanumeric(word):
    if(len(re.findall('\w+',word))>0):
        return True
    else:
        return False

def get_words_of_text(text):
    stop = set(stopwords.words('english'))
    puncts = set(string.punctuation)
    words = nltk.word_tokenize(text)
    ret = []
    temp = set(words) - stop - puncts
    for w in temp:
        if(word_has_alphanumeric(w)):
            w = re.sub('['+string.punctuation+']','',w)
            ret.append(w)
    return ret

def get_dictionary(texts):
    ret = {}
    i = 0
    for text in texts:
        text = text.lower().decode('utf8')
        rest = set(get_words_of_text(text)) - set(ret)
        for item in rest:
            if(item in ret.keys()):
                ret[item] += 1
            else:
                ret[item] = 1
        i += 1
        print('Finished '+str(i)+' of '+str(len(texts)))
    return ret

def get_texts_with_greater_len(data, thresh):
    ret = []
    for dato in data:
        for k in dato[1].keys():
            t = dato[1][k]
            if(len(t) >= thresh ):
                ret.extend(t)
    return ret

def extend_array(array, length):
    tail = [0] * (length - len(array))
    ret = array
    ret.extend(tail)
    return ret

def text_to_numbers(text, dictionary, max_text_len):
    words = get_words_of_text(text)
    t = []
    for w in words:
        if(w in dictionary):
            t.append(dictionary.index(w))
    ret = extend_array(t, max_text_len)
    return ret

def get_stats(data):
    ret = {}
    for item in data:
        for k in item[1].keys():
            l = len(item[1][k])
            if(l in ret.keys()):
                ret[l] +=1
            else:
                ret[l] = 1
    return ret

data = pickle.load(open( '/home/dpappas/scripts_dict.p', 'rb'))

texts = get_texts_with_greater_len(data, 50)

dictionary = get_dictionary(texts)

max_text_len = max(  [ len(text) for text in texts ]  )

text_to_numbers(data[0][1]['TEACHER'][0], dictionary.keys(), max_text_len)




























