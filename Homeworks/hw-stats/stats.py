#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv

def stats(x, x_mean, x_std):
    from math import sqrt
    n, sum, mean, std, min, max, median,zscore = len(x),0, 0, 0, 0 ,0,0,0
    for a in x:
        if isinstance(a, basestring):
            a = x[a]
	sum +=a
        if a<min:
            min = a
        if a>max:
            max = a
    mean = round(sum / float(n),2)
    for a in x:
        if isinstance(a, basestring):
            a = x[a]
	std = std + (a - mean)**2
    if n>1:
        std = round(sqrt(std / float(n-1)),2)
    sort_x = sorted(x)
    if not isinstance(sort_x[0], basestring):
        if n%2==0 :
            median = (sort_x[n/2]+sort_x[n/2-1])/2
        else:
            median = (sort_x[(n-1)/2])
    if x_std!=0 and not (x_std is None) and not (x_mean is None):
        zscore = round((sum-x_mean)/x_std,2)
    return n, sum, mean, min, max, median, std, zscore

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    norm = (value-min)/(max-min)
   # print "%s:\t %s" % (value, norm)
    ###/
    return round(norm,3)
def print_candidate_stats(stat, canSum):
    print "ID\tTotal\tMax\tMin\tMean\tMedian\tStd Dev\tZ-Score"
    cCount, cSum, cMean,cMin,cMax,cMedian,cStd,cZscore = stats(canSum, None, None);
  
    for candidate in stat:
        count, sum, mean, min, max, median, std, zscore= stats(stat[candidate], cMean, cStd)
        print "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (candidate,sum, max, min, mean, median, std, zscore)

numList = []
canList=[]
canStat = {}
canSum = {}
candidates = ""

for row in csv.reader(fileinput.input(), delimiter='|'):
    #if not fileinput.isfirstline():
        candidate = row[16]
        num = float(row[14])
        numList.append(num)
        if not candidate in canList:
            canStat[candidate]=[]
            canSum[candidate]=0
        canStat[candidate].append(num)
        canList.append(candidate)
        canSum[candidate]+=num

canList = set(canList)
count, sum, mean, min, max, median, std, zscore = stats(numList, None, None)

##### Print out the stats
print "Total: %s" % sum
print "Count: %s" % count
print "Minimum: %s" % min
print "Maximum: %s" % max
print "Mean: %s" % mean
print "Median: %s" % median
# square root can be calculated with N**0.5
print "Standard Deviation: %s" % std
#print "Z-Score: %s" % zscore
##### Comma separated list of unique candidate ID numbers
candidates = ", ".join(map(str, canList))
print "Candidates (%s): %s" % (len(canList), candidates)
 
##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
#print "Min-max normalized values: %r" % map(minmax_normalize, sortedNumList[::10])
print_candidate_stats(canStat,canSum)