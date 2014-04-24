#! /usr/bin/python

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="Jannah"
__date__ ="$Mar 3, 2014 9:19:43 PM$"
import math

def sigmoid(x):
    return 1/(1+math.exp(-x))

target =0
learn =10
#nodes = {'input':{'a':1,'b':2}, 'hidden':{'c':0.7311,'d':0.0179,'e':0.9933}, 'output':{'f':0.8387}}
input={'a':1,'b':2}
hidden={'c':0,'d':0,'e':0}
output={'f':target+1}
w = {'ac':-3,'ad':2,'ae':4, 'bc':2, 'bd':-3, 'be':.5, 'cf':.2, 'df':0.7,'ef':1.5};
err = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0}
#err['f']=nodes['output']['f']*(1-nodes['output']['f'])*(target - nodes['output']['f']);

#print err['f']
count = 0
#while abs(err['f'])>0.0000001 or count==0:
while abs(target-output['f'])>0.01 or count==0:
    count+=1
    ### PUSHING Output
    for o in output:
        output[o]=0
        for h in hidden:
            hidden[h]=0
            for i in input:
                weight = w[i+h]
                hidden[h]+=input[i]*weight
            hidden[h]=sigmoid(hidden[h])
            output[o]+=hidden[h]*w[h+o]
        output[o]=sigmoid(output[o])
        err[o]=output[o]*(1-output[o])*(target-output[o])
        for h in hidden:
            err[h]=hidden[h]*(1-hidden[h])*err[o]*w[h+o]
            w[h+o]=w[h+o]+learn*err[o]*hidden[h]
            for i in input:
                w[i+h]=w[i+h]+learn*err[h]*input[i]

    if count >0:
		out = "%s" % count
		titles="count"
		for h in hidden:
			out+=",%.8f" % hidden[h]
			titles+=",O%s" % h
		#out+=",W:,"

		for wt in w:
			out+=",%.8f" % w[wt]
			titles+=",W%s" % wt
		for e in err:
			out+=",%.8f" % err[e]
			titles+=",Err%s" % e
		for o in output:
			out+=",%.8f" % output[o]
			titles+=",O%s" % o

		if count==1:
			titles= titles.replace('a', '1')
			titles= titles.replace('b', '2')
			titles= titles.replace('c', '3')
			titles= titles.replace('d', '4')
			titles= titles.replace('e', '5')
			titles= titles.replace('f', '6')
			print titles
		print out
        #print hidden
        #print output
        #print err
        #print w
        #print err['f']
print count
print hidden
print output
print err
print w



