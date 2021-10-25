#!/bin/python3
import random
import copy
import timeit
from math import ceil
from statistics import mean
import matplotlib.pyplot as plt
import numpy as np
import sys


print('Started')

def sort_merge(lists):
    while len(lists)>1:
        nextlist = [None]*ceil(len(lists)/2.0)
        for x in range(ceil(len(lists)/2.0)):
            if (x*2+1)>=(ceil(len(lists)/2.0)):
                #If odd number of arrays, carry last array to next step
                nextlist[x] = lists[x*2]
            else:
                nextlist[x] = merge(lists[x*2],lists[x*2+1])
        lists = nextlist
    return lists[0]
        
def merge(a,b):
    merged = []
    if not isinstance(a,list):
        a = [a]
    if not isinstance(b,list):
        b = [b]
    while a or b:
        if a[0]<b[0]:
            merged.append(a[0])
            a.pop(0)
        elif a[0]>=b[0]:
            merged.append(b[0])
            b.pop(0)
        #If one array is empty append the second one
        if not a:
            for bi in b:
                merged.append(bi)
            b = []
        elif not b:
            for ai in a:
                merged.append(ai)
            a=[]
    return merged

def sort_selection(unsorted):
    while len(unsorted)>0:
        i = 0
        for ii in range(len(unsorted)):
            i = ii if unsorted[ii]<unsorted[i] else i
        if not 'sorted' in locals():
            sorted = [unsorted[i]]
            unsorted.pop(i)
        else:
            sorted.append(unsorted[i])
            unsorted.pop(i)
    return sorted

def sort_bubble(sortinglist):
    issorted = False
    while not issorted:
        issorted = True
        for i in range(1,len(sortinglist)):
            if sortinglist[i-1]>sortinglist[i]:
                issorted = False
                a = sortinglist[i-1]
                sortinglist[i-1] = sortinglist[i]
                sortinglist[i] = a
    return sortinglist



values = [10000,100000,1000000]
rep = 100
mergedtime=[[],[],[]]
bubbledtime = [[],[],[]]
selectiontime = [[],[],[]]
inputlist = []
for n in range(3):
    for repetition in range(rep):
        print('{}. run with {} values'.format(repetition+1,values[n]))
        inputlist = []
        for i in range(values[n]):
            inputlist.append(random.random()*1000)


        sinputlist = copy.deepcopy(inputlist)
        binputlist = copy.deepcopy(inputlist)
        minputlist = copy.deepcopy(inputlist)
        print('\tMerge sort')
        mergedtime[n].append(timeit.timeit(stmt='sort_merge(minputlist)',number=1,globals=globals()))
        print('\t\tMerge sort took {}s'.format(mergedtime[n][repetition]))
        print('\tBubble sort')
        bubbledtime[n].append(timeit.timeit(stmt='sort_bubble(binputlist)',number=1,globals=globals()))
        print('\t\tBubble sort took {}s'.format(bubbledtime[n][repetition]))
        print('\tSelection sort')
        selectiontime[n].append(timeit.timeit(stmt='sort_selection(sinputlist)',number=1,globals=globals()))
        print('\t\tSelection sort took {}s'.format(selectiontime[n][repetition]))

for i in range(3):
    mergedtime[i]=round(mean(mergedtime[i])*1000.0)/1000.0
    bubbledtime[i]=round(mean(bubbledtime[i])*1000.0)/1000.0
    selectiontime[i]=round(mean(selectiontime[i])*1000.0)/1000.0

fig,ax = plt.subplots()
width = 0.2
x = np.arange(len(values))
r1 = ax.bar(x-width,mergedtime,width=width,label='Merge sort')
r2 = ax.bar(x,bubbledtime,width=width,label='Bubble sort')
r3 = ax.bar(x+width,selectiontime,width=width,label='Selection sort')
ax.set_ylabel('Time [s]')
ax.set_xlabel('Number of elements')
ax.set_title('Sorting algorithms comparison')
ax.set_xticks(x)
ax.set_xticklabels(values)
ax.legend()
ax.bar_label(r1, padding=3)
ax.bar_label(r2, padding=3)
ax.bar_label(r3, padding=3)
fig.tight_layout()
plt.show()

print('done')
input('Press enter to terminate')