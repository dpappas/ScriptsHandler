#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pickle
data = pickle.load(open( '/home/dpappas/scripts_dict.p', 'rb'))

import string
import re
from pprint import pprint


def replace_numbers(text):
    text = re.sub(r'[-+]?\d*\.\d+','  _double_  ',text)
    text = re.sub(r'[-+]?\d+','  _integer_  ',text)
    return text

def fix_text(text):
    puncs = string.punctuation+'«»“”‘’—§›¶…΄·'
    text = replace_numbers(text)
    text = re.sub( r'<!--.*-->','',text , flags=re.DOTALL)
    text = re.sub('<.*?>','',text)
    text = re.sub('\(.*?\)','',text, flags=re.DOTALL)
    text = text.lower()
    text = re.sub(r'(['+puncs+'])',r' \1 ',text)
    l = -3
    while(len(text)!=l):
        l = len(text)
        text = re.sub(r'(['+puncs+'])  (['+puncs+'])',r'\1\2',text)
    text = text.replace('_ double _','_double_')
    text = text.replace('_ integer _','_integer_')
    text = re.sub("\s+"," ",text)
    return text

held_out = {}
total_tokens = 0
for dato in data:
    title = dato[0].replace(' ','_')
    for role in dato[1].keys():
        try:
            l = len(fix_text(' '.join( dato[1][role]) ).split())
            if(l>2000):
                total_tokens+=l
                held_out[title+'_'+role.replace(' ','_')] = dato[1][role]
        except:
            print(dato[0])
            print(role)

print(total_tokens)
pprint(held_out.keys())
pickle.dump(held_out,open('held_out_scripts.p','wb'))

























