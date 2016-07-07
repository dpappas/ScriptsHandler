#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from pprint import pprint
import re
from os import listdir
from os.path import isfile, join
import sys
from traceback import format_exc
import string

def count_spaces_on_start_of(s):
    m = 0
    for i in range(len(s)):
        if(s[i] == ' '):
            m+=1
        elif(s[i] == '\t'):
            m+=4
        else:
            return m
    return 0

def get_line_counts(scr):
    scr = re.sub( r'<!--.*-->','',scr , flags=re.DOTALL)
    scr = re.sub('<.*?>','',scr)
    lines = scr.split('\n')
    t = {}
    for line in lines:
        tem = count_spaces_on_start_of(line)
        if(tem in t.keys()):
            t[tem]+=1
        else:
            t[tem] = 1
    return t

def get_lines(dato):
    # clear script and get lines
    scr = dato['script']
    scr = re.sub( r'<!--.*-->','',scr , flags=re.DOTALL)
    scr = re.sub('<.*?>','',scr)
    scr = re.sub('\(.*?\)','',scr, flags=re.DOTALL)
    lines = scr.split('\n')
    lines = [ l for l in lines if(len(l.strip())>0)]
    return lines

def count_dupl_lines(lines):
    # count duplicate lines
    d = {}
    for line in lines:
        if(len(line.strip())>0):
            if(line in d.keys()):
                d[line]+=1
            else:
                d[line]=1
    return d

def max_count_spaces(d):
    # find max count of spaces on start for specific lines
    t = list(d.values())
    t = [x for x in t if(x>10)]
    m = {}
    for l in d.keys():
        if(d[l] in t):
            tem = count_spaces_on_start_of(l)
            if(tem in m.keys()):
                m[tem] += 1
            else:
                m[tem] = 1
    ma = max(m.values())
    f = [ k for k in m.keys() if(m[k] == ma) ][0]
    return f

def get_next_lines_count(lines,f):
    eg = {}
    for i in range(len(lines)):
        line = lines[i]
        if( count_spaces_on_start_of(line) == f ):
            if(i+1 < len(lines)):
                tem = count_spaces_on_start_of(lines[i+1])
                if(tem in eg.keys()):
                    eg[tem] += 1
                else:
                    eg[tem] = 1
    ma = max(eg.values())
    nl = [ k for k in eg.keys() if(eg[k] == ma) ][0]
    return nl

def get_names_and_speech(lines,f,nl):
    ret = ''
    for line in lines:
        tem = count_spaces_on_start_of(line)
        # if( ( tem == f ) or ( tem == nl ) or (len(line.strip())==0) ):
        #     ret += '\n'+line
        if( tem == f ):
            ret += '\n'+line
        if ( tem == nl ):
            ret += '\n'+line
    return ret.strip()

def get_one_output(lines):
    ret = ''
    i = 0
    while(i<len(lines)):
        line = lines[i]
        if(count_spaces_on_start_of(line) == f):
            while(len(line.strip())!=0):
                ret += '\n'+(line)
                i+=1
                if(i<len(lines)):
                    line = lines[i]
                else:
                    line = ''
        i+=1
    return ret.strip()

def get_script_as_dic(lines,f,nl):
    ret = {}
    name = ''
    text = ''
    for line in lines:
        tem = count_spaces_on_start_of(line)
        if( tem == f ):
            if((len(name.strip())>0) and (len(text.strip())>0) ):
                if(name in ret.keys()):
                    ret[name].append(text.strip())
                    name = ''
                    text = ''
                else:
                    ret[name] = [text.strip()]
                    name = ''
                    text = ''
            name = line.strip()
            name = re.sub('\(.*?\)','',name)
        if ( tem == nl ):
            text += ' '+line.strip()
    if(len(name.strip())>0):
        if(name in ret.keys()):
            ret[name].append(text)
        else:
            ret[name] = [text]
    return ret

def get_files_of_folder(directory):
    # return [directory+f for f in listdir(directory) if isfile(join(directory, f))]
    return [f.replace('.txt','').strip() for f in listdir(directory) if isfile(join(directory, f))]

def replace_numbers(text):
    text = re.sub(r'[-+]?\d*\.\d+','  _double_  ',text)
    text = re.sub(r'[-+]?\d+','  _integer_  ',text)
    return text

def fix_text(text):
    text = text.lower()
    puncs = string.punctuation+u'«»“”‘’—§›¶…΄·'
    text = re.sub(r'(['+puncs+'])',r' \1 ',text)
    l = -3
    while(len(text)!=l):
        l = len(text)
        text = re.sub(r'(['+puncs+'])  (['+puncs+'])',r'\1\2',text)
    replace_numbers(text)
    text = re.sub("\s+"," ",text)
    return text.replace('\n',' ')

dirr = '/home/dpappas/gate_processed_new/'

directory = '/home/dpappas/scripts_held_out'

fs = get_files_of_folder(directory)

# pprint(fs)

data = pickle.load(open( '/home/dpappas/script_data.p', 'rb'))

ret = []
for dato in data:
    try:
        if(dato['title'].strip() in fs):
            # dato = data[125]
            lines = get_lines(dato)
            d = count_dupl_lines(lines)
            # to f einai to count twn spaces gia names
            f = max_count_spaces(d)
            # vlepw h epomenh grammh meta to onoma ti count exei kai to onomazw nl
            nl = get_next_lines_count(lines,f)
            # tem = (get_names_and_speech(lines,f,nl))
            print(dato['title'].strip())
            r = get_script_as_dic(lines,f,nl)
            ret.append((dato['title'].strip(),r))
        # print(tem)
        # print(dato['link'])
        #     with open(dirr+dato['title']+'.txt','w') as f:
        #     f.write(tem)
        # f.close()
        # break
    except:
        # None
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print('Error for : ')
        # pprint(dato)
        print( exc_value )
        print( format_exc() )
# lines = tem.split('\n')
# print(get_one_output(lines))

# pprint(ret)

'''
print(r.keys())

for item in r.keys():
    print(item +'    '+str(len(r[item])))

pprint(r['TED'])
'''

pickle.dump( ret, open( '/home/dpappas/scripts_dict.p', "wb" ) )


























































