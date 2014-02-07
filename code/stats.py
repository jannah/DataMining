#!/usr/bin/python
"""This script can be used to analyze data in the 2012 Presidential Campaign,
<<<<<<< HEAD
available from http://www.fec.gov/disclosurep/PDownload.do"""
=======
available from ftp://ftp.fec.gov/FEC/2012/pas212.zip - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""
>>>>>>> 133528c07f2af5e51cca611a572c9a74e7003eee

import fileinput
import csv

<<<<<<< HEAD
total = 0

for row in csv.reader(fileinput.input()):
    if not fileinput.isfirstline():
        total += float(row[9])
=======
total = 0.0

for row in csv.reader(fileinput.input(), delimiter='|'):
    if not fileinput.isfirstline():
        total += float(row[14])
>>>>>>> 133528c07f2af5e51cca611a572c9a74e7003eee
        ###
        # TODO: calculate other statistics here
        # You may need to store numbers in an array to access them together
        ##/

###
# TODO: aggregate any stored numbers here
#
##/

##### Print out the stats
print "Total: %s" % total
print "Minimum: "
print "Maximum: "
print "Mean: "
print "Median: "
# square root can be calculated with N**0.5
print "Standard Deviation: "

<<<<<<< HEAD
##### Comma separated list of unique candidate names
=======
##### Comma separated list of unique candidate ID numbers
>>>>>>> 133528c07f2af5e51cca611a572c9a74e7003eee
print "Candidates: "

def minmax_normalize(value):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    ###
    # TODO: replace line below with the actual calculations
    norm = value
    ###/
<<<<<<< HEAD
    
=======

>>>>>>> 133528c07f2af5e51cca611a572c9a74e7003eee
    return norm

##### Normalize some sample values
print "Min-max normalized values: %r" % map(minmax_normalize, [2500, 50, 250, 35, 8, 100, 19])
<<<<<<< HEAD

=======
>>>>>>> 133528c07f2af5e51cca611a572c9a74e7003eee
