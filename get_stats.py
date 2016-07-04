#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
import re
import string
import numpy as np
import matplotlib.pyplot as plt
# plt.gca().tight_layout()
from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

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
    #+u'«»'
    text = re.sub(r'(['+string.punctuation+'])',r' \1 ',text)
    l = -3
    while(len(text)!=l):
        l = len(text)
        text = re.sub(r'(['+string.punctuation+'])  (['+string.punctuation+'])',r'\1\2',text)
    text = text.replace('_ double _','_double_')
    text = text.replace('_ integer _','_integer_')
    text = re.sub("\s+"," ",text)
    return text

def get_line_stats(data):
    ret = {}
    for item in data:
        for k in item[1].keys():
            l = len(item[1][k])
            if(l in ret.keys()):
                ret[l] +=1
            else:
                ret[l] = 1
    return ret

def get_token_stats(data):
    ret = {}
    for item in data:
        for k in item[1].keys():
            text = ' '.join(item[1][k])
            text = fix_text(text)
            l = len(text.split())
            if(l in ret.keys()):
                ret[l] +=1
            else:
                ret[l] = 1
    return ret

data = pickle.load(open( '/home/dpappas/scripts_dict.p', "rb" ) )


# N = 0
# ys = []
# labels = []
# stats = get_line_stats(data)
# for i in range(0, max(stats.keys()), 100):
#     too = min(i+100, max(stats.keys()))
#     s = sum([ stats[m] for m in stats.keys() if(m>i and m<=too)])
#     print(i,too,s)
#     labels.append(str(i)+' to '+str(too))
#     ys.append(s)
#     N+=1
#
# ind = np.arange(N)
# width = 1
# p1 = plt.bar(ind, ys, width, color='b')
# plt.ylabel('Number of Users')
# plt.xlabel('Number of Lines')
# plt.title('Number of Users per Number of Lines')
# plt.xticks(ind + width/2, labels, rotation='vertical')
# # plt.show()
# plt.savefig('users_per_lines_number.png')


# print('')
# N = 0
# ys = []
# labels = []
# stats = get_token_stats(data)
# for i in range(0, max(stats.keys()), 300):
#     if(i==2700):
#         too = max(stats.keys())
#         s = sum([ stats[m] for m in stats.keys() if(m>i and m<=too)])
#         print(i,too,s)
#         labels.append(str(i)+' to '+str(too))
#         ys.append(s)
#         N+=1
#         break
#     else:
#         too = min(i+300, max(stats.keys()))
#         s = sum([ stats[m] for m in stats.keys() if(m>i and m<=too)])
#         print(i,too,s)
#         labels.append(str(i)+' to '+str(too))
#         ys.append(s)
#         N+=1


print('')
N = 0
ys = []
labels = []
stats = get_token_stats(data)
for i in range(0, max(stats.keys()), 300):
    too = min(i+300, max(stats.keys()))
    s = sum([ stats[m] for m in stats.keys() if(m>i and m<=too)])
    print(i,too,s)
    labels.append(str(i)+' to '+str(too))
    ys.append(s)
    N+=1

ind = np.arange(N)
width = 0.3
p1 = plt.bar(ind, ys, width, color='b')
plt.ylabel('Number of Users')
plt.xlabel('Number of Tokens')
plt.title('Number of Users per Number of Tokens')
plt.xticks(ind + width/2, labels, rotation='vertical', fontsize=7)
# plt.show()
plt.savefig('users_per_tokens_number.png')


# len(data)
# m = 0
#
#
# for item in data:
#     m+= len([ k for k in item[1].keys() if(len(item[1][k])>20 ) ])
# print(m)
#
#
# attakes = []
# for item in data:
#     t = item[1].keys()
#     for k in t:
#         attakes.append(len(item[1][k]))
# attakes.sort()
#
# tokens_size = []
# for item in data:
#     t = item[1].keys()
#     for k in t:
#         s = 0
#         for sent in item[1][k]:
#             s += len(fix_text(sent).split())
#         tokens_size.append(s)
# tokens_size.sort()
#
# print(np.mean(tokens_size))
# print(np.max(tokens_size))
# print(np.std(tokens_size))
# print(np.median(tokens_size))
#
# import matplotlib.mlab as mlab
# import matplotlib.pyplot as plt
#
#
#
# mu = np.mean(attakes)
# sigma = np.std(attakes)
#
# n, bins, patches = plt.hist(attakes, 30, normed=1, facecolor='green', alpha=0.75)
# # n, bins, patches = plt.hist(tokens_size, 100, facecolor='green')
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)
# plt.xlabel('Lines')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ Lines:}\ \mu='+str(mu)+',\ \sigma='+str(sigma)+'$')
# plt.axis([0, 400, 0, 0.04])
# plt.grid(True)
# plt.savefig('Lines_histogram.png', bbox_inches='tight')
# plt.show()
#
#
#
# mu = np.mean(tokens_size)
# sigma = np.std(tokens_size)
# n, bins, patches = plt.hist(tokens_size, 120, normed=1, facecolor='green', alpha=0.75)
# # n, bins, patches = plt.hist(tokens_size, 100, facecolor='green')
# y = mlab.normpdf( bins, mu, sigma)
# l = plt.plot(bins, y, 'r--', linewidth=1)
# plt.xlabel('Tokens')
# plt.ylabel('Probability')
# plt.title(r'$\mathrm{Histogram\ of\ Tokens:}\ \mu='+str(mu)+',\ \sigma='+str(sigma)+'$')
# plt.axis([0, 3000, 0, 0.006])
# plt.grid(True)
# plt.savefig('Tokens_histogram.png', bbox_inches='tight')
# plt.show()
#















