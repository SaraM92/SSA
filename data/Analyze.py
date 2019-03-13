###############################################################
#This script is written by:
#Sara A. Metwalli
#For Hara Lab in Tokyo Institute of Technology
##
#This script performs the systematic analysis
################################################################
#Libraries needed
from sympy import *
from string import *
import re
################################################################

#Constants, variables intialization 
f = open("KLEEout_converted.txt","r")
OpValue = {'*': 4, '**':4, '^':4, '+':3, '-':3, '/':2}
myList = []
original_exprs =[]
simplified_exprs = []
tempDict = {}
exprsList =[]
exprsList_coff =[]
weights = []
vals =[]
occur= {}
op_weight = {}
keyz =[]
total_weight={}
total_weight_sorted ={}

################################################################
# INPUT
for line in f:
    myList.append(line)

for expr in myList:
  original_exprs.append(sympify(expr))
#For debugging purposes
#print ("Original Expressions ",original_exprs)
#print ("=====================================================")
for expr in original_exprs:
  simplified_exprs.append(simplify(expr))
#For debugging purposes
#print ("Simplified Expressions ",simplified_exprs)
#print ("=====================================================")

################################################################
# GET LR-BASED WEIGHT
#STEP ONE: GET COFFS
for i in simplified_exprs:
  process = i.as_coefficients_dict()
  tempDict = process.copy()
  exprsList.append(tempDict.copy())
#For debugging purposes
#print ("Dict for Coff",exprsList)
#print ("============================================================")
#STEP TWO: REMOVE CONSTANTS
for item in exprsList:
  if 1 in item.keys():
    item.pop(1,0)
  exprsList_coff.append(item)
#For debugging purposes
#print("Dict for coff after removing consts",exprsList_coff)
#print ("============================================================")
#STEP THREE: GET WEIGHTS
for item in exprsList_coff:
  tempDict.clear()
  for val in item.values():
      if val <0:
        vals.append(abs(val))
      else:
        vals.append(val)
  dimm = sum(vals)
  del vals[:]
  for k in item.keys():
    w = item[k]/dimm
    tempDict[k] = abs(w)
  weights.append(tempDict.copy())
#For debugging purposes
#print("weights",weights)
#print ("============================================================")

################################################################
#GET OCCURANCE-BASED WEIGHT
#STEP ONE: GET ALL POSSIBLE VARIABLES
#print (exprsList)
for item in exprsList_coff:
#  print (item)
  for key in item:
    if key not in keyz:
      keyz.append(key)
#STEP TWO: INIT DICT FOR WEIGHT
for key in keyz:
  occur[key]=0
#STEP THREE: CLACULATE WEIGHT
for item in exprsList_coff:
  for key in keyz:
    if key in item.keys():
      occur[key] += 1
#STEP FOUR: NORMALIZE weights
for key in occur.keys():
  occur[key]= occur[key]/sum(occur.values())
#For debugging purposes
#print ("Occurance Based Weight",occur)
#print ("============================================================")

################################################################
#GET OPERATIONS-BASED WEIGHT
#STEP ONE: INIT WEIGHT DICT
for key in keyz:
  op_weight[key]=0
#STEP TWO: CALCULATE WEIGHT
for item in simplified_exprs:
  for key in OpValue:
    if key in str(item):
      for l in op_weight:
        op_weight[l] += OpValue[key]
#STEP THREE: NORMALIZE WEIGHTS
for key in op_weight.keys():
  op_weight[key] = op_weight[key]/sum(op_weight.values())
#For debugging purposes
#print ("Operation Based Weigth", op_weight)
#print ("============================================================")
################################################################
#GET OVERALL WEIGHT FOR EVERY VARIABLE
#STEP ONE: INIT THE DICT
for key in keyz:
  total_weight[key]=0
#STEP TWO: CALCULATE TOTAL LR-BASED WEIGHT
for key in total_weight:
  for item in weights:
    if key in item:
      total_weight[key] += item[key]
#STEP THREE: ADD OCCURANCE-BASED WEIGHT
for key in total_weight:
  total_weight[key] += occur[key]
#STEP FOUR: ADD OPERATIONS-BASED WEIGHT
for key in total_weight:
  total_weight[key] += op_weight[key]
#For debugging purposes
#print ("Total Weight", total_weight)
#print ("=====================================================")

################################################################
#SORT THE OVERALL WEIGHT
for i in sorted(total_weight.values()):
  for key in total_weight:
    if total_weight[key] == i:
      total_weight_sorted[key] = int(round(i))
#For debugging purposes
#print ("Sorted", total_weight_sorted)


