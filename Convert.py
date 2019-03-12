################################################################
#This script is written by
#Sara A. Metwalli
#For Hara Lab in Tokyo Institute of Technology
#
#This script is to convert the KLEE output to readable math format
################################################################
#Needed library
from string import *
import re
import itertools
################################################################
#list identification for possible operations
# arithmetic operations
ArithOp = {'Add':'+','Sub':'-','Mul':'*','UDiv':'/','URem':'%','SDiv':'/','SRem':'%'}
#bitwise operations
BitwiseOp = ["Not","And","Or","Xor","Shl","LShr","AShr"]
#Comparisions Operations
CompOp = ["Eq","Ne","Ult","Ule","Ugt","Uge","Slt","Sle","Sgt","Sge"]
#sizes
sizes = {'w32':'int','w8':'char'}
#macro forms
macro = ["ReadLSB","ReadMSB"]
################################################################
#Variables initializtion and constants statement
#empty dic
order ={}
#names
input_lines=[]
input_lines_clean=[]
input_lines_afop=[]
input_lines_afvars1=[]
em_dict={}
size_of_vars = ''
out =''
read_line=''
symbolic_vars_uncut =[]
symbolic_vars =[]
input_lines_aflvl1 =[]
input_lines_aflvl2 =[]
input_lines_aflvl3 =[]
matches =[]
temp_list=[]
exprs ={}
################################################################

#input
with open('KLEEout_clean.txt','r') as myFile:
        for line in myFile:
                read_line = read_line +line
read_line = read_line.rstrip()
#For debugging purposes
#print ("-----------------------------------------------------")
#print ("The input query is:", read_line)
#print ("-----------------------------------------------------")
################################################################

#Getting rid of ReadLSB
for item in macro:
        if item in read_line:
                out = read_line.replace(item,'')
input_lines = out.split('\n')
#For debugging purposes
#print ("-----------------------------------------------------")
#print (input_lines)
################################################################

#to get the size of variables
# we need to add the variable name to this!
for key in sizes:
        for item in input_lines:
                if key in item:
                        kee = key +' '
                        input_lines_clean.append(item.replace(kee,''))
                        size_of_vars += sizes[key]
#For debugging purposes
#print ("-----------------------------------------------------")
#print ("line after size finding", input_lines_clean)
################################################################

#get the the symbolic variables in the output/s
symexpr = re.compile(r'\d+\s\w+')
for item in input_lines_clean:  
        dummy1 = symexpr.findall(item)
        symbolic_vars_uncut.append(dummy1)
number_of_sym_vars = len(symbolic_vars_uncut)
#For debugging purposes
#print ("there is/are", number_of_sym_vars, "output/s in this program and the sym vars they depend on is/are", symbolic_vars_uncut)
#print ("-----------------------------------------------------")
################################################################

for item in symbolic_vars_uncut:
        em_dict.clear()
        for i in range(0, len(item)):
                dummy2 = item[i].split()
                n_key = dummy2[1]
                n_value = dummy2[0]
                em_dict[n_key] = n_value
        symbolic_vars.append(em_dict.copy())
#For debugging purposes
#print ("the vars based on the output", symbolic_vars)
#print ("-----------------------------------------------------")
################################################################

# PUTTING THE EXPR IN SHAPE
for item in input_lines_clean:
  item = item.replace(")",") ")
  item = item.replace("(", " (")
  temp = item.rstrip().lstrip()
  input_lines_afop.append(' '.join(temp.split()))
#remove the place of the sym vars
symexpr = re.compile(r'\(\s\d+\s(\w+)\)')
for item in input_lines_afop: #input_lines_clean instead of input_lines_afop
        l = symexpr.findall(item)
        input_lines_afvars1.append(symexpr.sub(r'\1', item))
#For debugging purposes
#print ("Line after removing vars", input_lines_afvars1)
#print ("-----------------------------------------------------")
################################################################

#LEVEL ONE
for query in input_lines_afvars1:
  for key in ArithOp:
    regexpr1 = r'\((' + re.escape(key) + r'(\s\w+)+)(\s)*\)'
    myregx = re.compile(regexpr1)
    if len(myregx.findall(query)) != 0:
      matches.append(myregx.findall(query))
  if len(matches)>0:
    if len(matches)!=1:
      matches[0]= [i for i in itertools.chain.from_iterable(matches)]
    for item in matches[0]:
      item_c = item[0]
      item_a = item_c
      ind = matches[0].index(item)
      item_a = item_a.replace("(","")
      item_a = item_a.replace(") ","")
      for key in sorted(ArithOp):
        if key in item_a:
          operation = ArithOp[key]
          kee = key+ " "
          item_a= item_a.replace(kee,"")
          temp_list = item_a.split()
          exprs[ind] = operation.join(temp_list)
          item_d = "("+item_c+" )"
          query_copy = query.replace(item_d,exprs[ind])
          if query_copy == query:
            item_d = "("+item_c+")"
            query = query.replace(item_d,exprs[ind])
          else:
            query = query.replace(item_d,exprs[ind])
  input_lines_aflvl1.append(query)
#For debugging purposes
#print ("After level 1",input_lines_aflvl1)
#print ("-----------------------------------------------------")
del matches[:]
################################################################

#LEVEL TWO
for query in input_lines_aflvl1:
  for key in ArithOp:
    regexpr2 = r'\((' + re.escape(key) + r'\s\w+(\W\w+)*\s\w+(\W\w+)*)+(\s)*\)'
    if len(re.compile(regexpr2).findall(query)) != 0:
      matches.append(re.compile(regexpr2).findall(query))
    if len(matches)>0:
      if len(matches)!=1:
        matches[0]= [i for i in itertools.chain.from_iterable(matches)]
      for item in matches[0]:
        item_c = item[0]
        item_a = item_c
        ind = matches[0].index(item)
        item_a = item_a.replace("(","")
        item_a = item_a.replace(")","")
        for key in sorted(ArithOp):
          if key in item_a:
            operation = ArithOp[key]
            kee = key+ " "
            item_a= item_a.replace(kee,"")
            temp_list = item_a.split()
            exprs[ind] = operation.join(temp_list)
            item_d = "("+item_c+" )"
            query_copy = query.replace(item_d,exprs[ind])
            if query_copy == query:
              item_d = "("+item_c+")"
              query = query.replace(item_d,exprs[ind])
            else:
              query = query.replace(item_d,exprs[ind])
  input_lines_aflvl2.append(query)
#For debugging purposes
print ("After level 2",input_lines_aflvl2)
#print ("====================================================")
del matches[:]
################################################################

#LEVEL THREE
for query in input_lines_aflvl2:
  while (any(key in query for key in ArithOp.keys())):
    for key in ArithOp:
      regexpr3 = r'\((' + re.escape(key) + r'(\s\w+)+(\W\w+)+)(\s)*\)'
      if len(re.compile(regexpr3).findall(query)) != 0:
        matches.append(re.compile(regexpr3).findall(query))
    if len(matches)>0:
      if len(matches)!=1:
          matches[0]= [i for i in itertools.chain.from_iterable(matches)]
      for item in matches[0]:
        item_c = item[0]
        item_a = item_c
        ind = matches[0].index(item)
        item_a = item_a.replace("(","")
        item_a = item_a.replace(")","")
        for key in sorted(ArithOp):
          if key in item_a:
            operation = ArithOp[key]
            kee = key+ " "
            item_a= item_a.replace(kee,"")
            temp_list = item_a.split()
            exprs[ind] = operation.join(temp_list)
            item_d = "("+item_c+" )"
            query_copy = query.replace(item_d,exprs[ind])
            if query_copy == query:
              item_d = "("+item_c+")"
              query = query.replace(item_d,exprs[ind])
            else:
              query = query.replace(item_d,exprs[ind])
  input_lines_aflvl3.append(query)
#For debugging purposes
#print ("After level 3",input_lines_aflvl3)
#print ("====================================================")
################################################################

#Write outputs to file
outFile = open("KLEEout_converted.txt","w")
for query in input_lines_aflvl3:
        outFile.write("%s\n" %query)
outFile.close()
