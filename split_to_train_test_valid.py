
import pickle
d = pickle.load(open('held_out_scripts.p','rb'))
print(len(d.keys()))  # 589 actors                2162749 tokens                 3672 meso oro
print(d.keys())
# print(d['Up_RUSSELL'])
# for k in d.keys():
#     print(len(d[k]))
print(min([len(d[k]) for k in d.keys()]))

test_set = {}
valid_set = {}
train_set = {}
for k in d.keys():
    too = int(round(len(d[k])*0.1)+1)
    test_set[k] = d[k][:too]
    fr = too
    too = fr+int(round(len(d[k])*0.1))+1
    valid_set[k] = d[k][fr:too]
    fr = too
    train_set[k] = d[k][fr:]

for k in d.keys():
    print(len(test_set[k]), len(valid_set[k]), len(train_set[k]))

pickle.dump(train_set,open('train_scripts.p','wb'))
pickle.dump(valid_set,open('valid_scripts.p','wb'))
pickle.dump(test_set,open('test_scripts.p','wb'))
