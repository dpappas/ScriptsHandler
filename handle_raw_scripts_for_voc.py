#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re
import string

def replace_numbers(text):
    text = re.sub(r'[-+]?\d*\.\d+','  _double_  ',text)
    text = re.sub(r'[-+]?\d+','  _integer_  ',text)
    return text

def fix_text(text):
    text = replace_numbers(text)
    text = re.sub( r'<!--.*-->','',text , flags=re.DOTALL)
    text = re.sub('<.*?>','',text)
    text = re.sub('\(.*?\)','',text, flags=re.DOTALL)
    text = text.lower()
    text = re.sub(r'(['+string.punctuation+'])',r' \1 ',text)
    l = -3
    while(len(text)!=l):
        l = len(text)
        text = re.sub(r'(['+string.punctuation+'])  (['+string.punctuation+'])',r'\1\2',text)
    text = text.replace('_ double _','_double_')
    text = text.replace('_ integer _','_integer_')
    text = re.sub("\s+"," ",text)
    return text

data = pickle.load(open( '/home/dpappas/script_data.p', 'rb'))

i = 0
all_text = ''
for dato in data:
    i += 1
    # print(dato.keys())
    dato['script'] = replace_numbers( dato['script'] )
    dato['script'] = fix_text( dato['script'] )
    # print(dato['script'])
    all_text += ' '+dato['script']
    print(str(i)+' of '+str(len(data)))

with open('all_scripts_together.txt','w') as f:
    f.write(all_text)
    f.close()
































