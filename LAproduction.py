#ReferenceV211.py   (s/b pyw?)
#inuts: Rulesin.txt: csv, from,to,fraction. Clostin: From, amountg
from pprint import pprint
import sys
print ( "LA Reference V2.1    ",sys.version )
print ("Released as-is, Open Source License.")
import csv
import copy
import math
import io
import decimal
import time
StartTime = time.time()
InFileName = 'rulesin.txt'
CostInFileName = 'costin.txt'
RulesOutFileName = 'rulesout.txt'
CostOutFileName = 'costout.txt'
TraceOutFileName = 'traceout.txt'
FracFmt = '{:>8.4}'
SmallestFraction = 0.0001 # tenth of a percent

SvcDepNamesSet= set( )
ProdDepNamesSet= set( )
SvcDepNamesList = [ ]
ProdDepNamesList = [ ]
DepNamesList = [ ]
NamesList = [ ]
SetDiff = set( )
NamesDict = { }
NumSvcDep  = 0; 
NumProdDep = 0
NumBoth = 0; 
indx = 0
toMatrix = [ ]     #Alternate matrices for iteration
fromMatrix  = [ ]  # ditto
AllocationPortion = 0.0
print ("rules 1st pass")
InFileVar = open(InFileName,'r')
LAreader = csv.reader(InFileVar)
for line in LAreader:
 	SvcDepNamesSet.add (line[0].strip())
 	ProdDepNamesSet.add (line[1].strip())
InFileVar.close
ProdDepNamesSet = set(ProdDepNamesSet - SvcDepNamesSet) 
NumSvcDep = len(SvcDepNamesSet)
NumProdDep = len(ProdDepNamesSet)
NumBoth = NumSvcDep + NumProdDep
SvcDepNamesList = list(SvcDepNamesSet)
SvcDepNamesList.sort(key=str.lower)
ProdDepNamesList = list(ProdDepNamesSet)
ProdDepNamesList.sort(key=str.lower)
NamesList = SvcDepNamesList + ProdDepNamesList
for i in range(NumBoth):
	NamesDict[NamesList[i]] = i
# Set matrices to zeros and ones
toMatrix  = [0.0] * NumBoth  #Establish dimensions
for i in range(NumBoth):
	toMatrix [i] = [0.0] * NumBoth
for indx in iter(range(NumSvcDep,NumBoth)):
	toMatrix [indx][indx] = 1.0
fromMatrix = toMatrix.copy()
print ("rules 2nd pass, iteration:")
InFileVar = open(InFileName,'r')
LAreader = csv.reader(InFileVar)
for line in LAreader:  
	fromName = line[0].strip()
	toName = line[1].strip()
	elementFraction = float(line[2].strip())
	toMatrix  [NamesDict[fromName]] [NamesDict[toName]] = elementFraction
	rowSS = NamesDict[fromName]
	colSS = NamesDict[toName]

# Matrix built, start iterations
SetMatrixTime = time.time()
print('time to complete matrix.   ', SetMatrixTime - StartTime)
def iterMM(toMatrix , fromMatrix ):  #do MM l91	toMatrix = iterMM(toMatrix , fromMatrix )

	fromMatrix  = toMatrix .copy()
	toMatrix  = [0.0] * NumBoth #see l62
	for i in range(NumBoth):
		toMatrix [i] = [0.0] * NumBoth		
# Actual iterations, still in iterMM
	for i in range(NumBoth):
		for k in range(NumBoth):
			if fromMatrix[i][k] >= 0.0001:
				for j in range(NumBoth):
					toMatrix [i][j] += fromMatrix[i][k] * fromMatrix [k][j]
	return(toMatrix)
#END of iterMM function		
for i in range(5):  # five iterations
	toMatrix = iterMM(toMatrix , fromMatrix )
	print (i)

RulesOutFileVar = open(RulesOutFileName,'w')
RulesOutWriter = csv.writer(RulesOutFileVar)
for i in range (NumSvcDep):
	for j in range(NumBoth):
		if toMatrix[i][j] < SmallestFraction:
			toMatrix[i][j] = 0.0
		else:
			RulesOutWriter.writerow([NamesList[i],
				NamesList[j], '{:.3f}'.format(toMatrix[i][j])])
				
TraceOutFileVar = open(TraceOutFileName, 'w')
TraceOutWriter = csv.writer(TraceOutFileVar)
AllocatedCosts = [0.0]*NumBoth
InFileVar = open(CostInFileName,'r')
LAreader = csv.reader(InFileVar)

for line in LAreader:
	fromName = line[0].strip()
	fromCost = float(line[1].strip())
	rowSS = NamesDict[fromName]
	for colSS in range(NumSvcDep, NumBoth):
		AllocationPortion = toMatrix[rowSS][colSS] * fromCost
		AllocatedCosts[colSS] += AllocationPortion
		TraceRow = [ fromName, NamesList[colSS], '{:.2f}'.format(AllocationPortion)]
		if len (line) == 3:
			TraceRow.append(line[2].strip())
		TraceOutWriter.writerow(TraceRow)
print ('Total allocated:', sum(AllocatedCosts))	
InFileVar.close	
CostsOutFileVar = open(CostOutFileName,'w')
CostsOutWriter = csv.writer(CostsOutFileVar)
for i in range(NumSvcDep, NumBoth):
	CostsOutWriter.writerow([NamesList[i],'{:.2f}'.format(AllocatedCosts[i])])
EndTime = time.time()
print ('Total time:  ',EndTime - StartTime)
print ('NEOJ')
