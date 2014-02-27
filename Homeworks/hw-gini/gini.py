#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
from collections import deque, defaultdict, Counter
from operator import itemgetter
import csv

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}

############### Set up variables
# TODO: declare datastructures
canTotal = Counter()
canByZip = {}
contributions = {}
contributionsTotal = Counter()
zipTotal = Counter()


for can in CANDIDATES:
    canByZip[CANDIDATES[can]] = Counter()
    contributions[CANDIDATES[can]] = Counter()
############### Read through files
for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue
        
    candidate_name = CANDIDATES[candidate_id]
    zip_code = row[ZIP_CODE]
    zip_code = zip_code[0:5]
    trans = float(row[TRANSACTION_AMT])

    ###
    # TODO: save information to calculate Gini Index
    ##/
    
    canTotal.update([candidate_name])
    zipTotal.update([zip_code])
    canByZip[candidate_name].update([zip_code])
    contributions[candidate_name].update([trans])
    contributionsTotal.update([trans])

###
# TODO: calculate the values below:
gini = 1  # current Gini Index using candidate name as the class
split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code
zip_gini = defaultdict(float)
#fracs = 0
sumCan = sum(canTotal.values())
sumZip = sum(zipTotal.values())
for can in canTotal.items():
    gini-= (can[1]/float(sumCan))**2
    zipList = dict(canByZip[can[0]])
    for zip in zipList:
        temp = (zipList[zip]/float(zipTotal[zip]))**2
        if zip not in zip_gini:
            zip_gini[zip]=1
        zip_gini[zip]-= temp

for can in canByZip:
    canByZip[can] = dict(canByZip[can])
#    print canByZip[can]
    
for zip_pair in zipTotal.items():
#    print zip_pair
    zip = zip_pair[0]
    zip_count = zip_pair[1]
    for can in canByZip:
#        print canByZip[can]
        temp = 0
        if zip  in canByZip[can]:
            temp = canByZip[can][zip]  
        temp_gini = temp/float(sumZip)*zip_gini[zip]
#        print  "%s has %s our of %s in zip %s (%.4f)" % (can,temp, sumZip, zip, temp_gini)
        split_gini+=temp_gini
    
##/



canSplits = {}
canSizes = defaultdict(int)
splitTotal = sum(contributionsTotal.values())
contributionsTotal = sorted(dict(contributionsTotal).items(), key=itemgetter(0))

### prepare candidates for splitting
canPlaceholders= {}
for can in contributions:
    canPlaceholders[can]=defaultdict(int)
    canPlaceholders[can]['sum'] = sum(contributions[can].values())
    temp = dict(contributions[can])
    contributions[can] = sorted(temp.items(), key=itemgetter(0))
    canSizes[can]= len(temp)

splitCount = len(contributionsTotal)
splits = {}
lowestSplit = {}
lowGini = {'point':0.0, 'value':1.0}
for x in range(0, splitCount-1):
    key = contributionsTotal[x][0]
#    value = contributionsTotal[x][1]
    nextKey = contributionsTotal[x+1][0]
#    nextValue = contributionsTotal[x+1][1]
    splitPoint = (key+nextKey)/float(2)
#    splitPoint = key
    splits[splitPoint]={'below': defaultdict(int), 'above':defaultdict(int),'gini':0}
    totalBelow = 0
    totalAbove = 0
    giniBelow = 1.0
    giniAbove = 1.0
    for can in contributions:
        
        splits[splitPoint]['below'][can]=canPlaceholders[can]['total']
#        print contributions[can][canPlaceholders[can]['index']][0]
        while canPlaceholders[can]['index']<canSizes[can] and contributions[can][canPlaceholders[can]['index']][0]<= splitPoint :
            tempValue = contributions[can][canPlaceholders[can]['index']][1]
            canPlaceholders[can]['index']+=1
            canPlaceholders[can]['total']+=tempValue
            splits[splitPoint]['below'][can]+=tempValue
        splits[splitPoint]['above'][can]=  canPlaceholders[can]['sum']-splits[splitPoint]['below'][can]
        totalBelow += splits[splitPoint]['below'][can]
        totalAbove += splits[splitPoint]['above'][can]
    total = totalBelow+totalAbove
    for can in contributions:
        giniBelow-= (splits[splitPoint]['below'][can]/float(totalBelow))**2
        giniAbove-= (splits[splitPoint]['above'][can]/float(totalAbove))**2
    
#    canPlaceholders[can]['sum']
    t_gini = giniBelow*totalBelow/total+giniAbove*totalAbove/total
    splits[splitPoint]['gini']= t_gini
    if t_gini<lowGini['value']:
        lowGini['value'] = t_gini
        lowGini['point'] = splitPoint
        lowestSplit = splits[splitPoint]



#print lowestSplit


# PURE OUTPUT for display
splits = sorted(dict(splits).items(), key=itemgetter(0))
print "Split,gini,belowR,belowO,total,aboveR,aboveO,total"
for split in splits:
#    y= "\t".join(str(e)+"\t"+str(canPlaceholders[e]['sum']) for e in canPlaceholders)
    temp = dict(split[1])
    s_gini = temp['gini']
    #if s_gini < lowGini:
     #   lowGini = s_gini
      #  lowestSplit = split
    str =[]
    str.append(split[0])
    str.append(s_gini)
    str.append(temp['below']['Romney']) 
    str.append(temp['below']['Obama'])
    str.append((temp['below']['Romney']+ temp['below']['Obama']))
    str.append(temp['above']['Obama'])
    str.append(temp['above']['Romney'])
    str.append((temp['above']['Obama']+temp['above']['Romney']))
    #print str
 

print "Gini Index: %s" % gini
print "Gini Index after split by zip: %s" % split_gini
print "Best Split for Contributions Amount is at %s (gini=%s)"% (lowGini['point'], lowGini['value'])
           
    