

import numpy as np
import pandas as pd
import copy

#all the data is stored as a list of lists
df = pd.read_csv("groceries.csv")
data = []
for row in range(0,9834):
    temp = []
    for item in df.iloc[row]:
        if(item == item):
            temp.append(item)
    data.append(temp)          

#set the desired support and confidence
#support is set as a percentage
#confidence is set as a fraction
supportThreshold = 1.0
confiThreshold = .5

#function to find the support of a given set of elements
def support(data,element):
    count = 0;
    for row in data:
        flag = 0
        item = list(element)
        for item in element:
            if item not in row:
                flag = 1
        if flag == 0:
            count+=1
    return count * 100/len(data)

#function to find number of unique single elements in the dataset (eg-yogurt,bottled water,etc)
def unique_items(data):
    temp = set()
    for row in data:
        for item in row:
            temp.add(item)
    return temp;

#function to find the number of unique elements in the dataset above the given support
def initial_items(unq):
    strt = []
    for item in unq:
        item = [item]
        if support(data,item) >= supportThreshold:
            item = set(item)
            strt.append(item)
    return strt

def separate(itemset):
    _ = set()
    for i in itemset:
        for item in i:
            _.add(item)
    return list(_)

def unique_list(L):
    return [set(item) for item in set(frozenset(item) for item in L)]

#function to perform the join operation of two sets while generating C[k+1]
def joinSet(itemSet):
    itemList = separate(itemSet)
    result = []
    for Set in itemSet:
        for item in itemList:
            temp = copy.copy(Set)
            if item in temp:
                continue
            temp.add(item)
            if temp in result:
                continue
            result.append(temp)
    return result


#funtion to prune sets from C[k+1] not appearing in L[k]
def prune(C, L):
    res = []
    for Set in C:
        ok = True
        for item in Set:
            if ok == False:
                break
            _set = copy.copy(Set)
            _set.remove(item)
            if _set not in L:
                ok = False
        if ok:
            res.append(Set)
    return res


#function to convert the set to string(used to create o/p file)
def SetToStr(S):
    _str = ''
    for item in S:
        _str += item
        _str += ','
    _str = _str[:-1]
    return '{' + _str + '}' + '[' + str(round(0.01 * len(data) * support(data, S))) + ']'

#function to create rules(used to create o/p file)
def convert(S, T):
    return SetToStr(S) + ' => ' + SetToStr(T)

#function to generate rules from a k-freqent set
def getConfidences(confidences, Set):
    
    _set = list(Set)
    n = len(_set)
    invalid = set()
    
    for mask in range(1 << n):
        _tmp = set()
        _tmp_ = set()
        
        ok = True
        for submask in invalid:
            if mask&submask == mask:
                ok = False
        if not ok:
            continue
        
        for i in range(n):
            if (1 << i) & mask:
                _tmp_.add(_set[i])
            else:
                _tmp.add(_set[i])

        if len(_tmp) == 0 or len(_tmp_) == 0:
            continue
        confi = support(data, Set) / support(data, _tmp)

        if (confi < confiThreshold):
            invalid.add(mask)
        else:
            confidences[convert(_tmp, _tmp_)] = confi


#function to find k-frequent sets
def Apriori(confidences, start, file):
    L = start[:]
    C = []
    C = joinSet(L)
    C = prune(C, L)
    Lnext = []
    for _set in C:
        if support(data,list(_set)) >= supportThreshold:
            Lnext.append(_set)
    if len(Lnext) == 0:
        return L
    else:
        print(len(Lnext))
        for Set in Lnext:
            file.write(SetToStr(Set))
            file.write('\n')
            getConfidences(confidences, Set)
        return Apriori(confidences, Lnext, file)


uni = unique_items(data)
init = initial_items(uni)
confidences = dict()
file = open('freq_itemset_sup=1_conf=5e-1.txt', 'w')#filename for frequent sets
res = Apriori(confidences, init, file)
file.close()

with open('assn_rules_sup=1_conf=5e-1.txt', 'w') as file: #filename for rules
    for a in confidences:
        file.write(a)
        file.write('  || confidence = ' + str(confidences[a]))
        file.write('\n')
print("completed")

