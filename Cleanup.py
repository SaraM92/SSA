################################################################
#This Scrip is written by:
#Sara A. Metwalli
#For Hara Lab in Tokyo Institute of Technology
#
#This script is used to cleanup the text resultant from KLEE to make it analyzable
################################################################
# cleaning up text file
import re
import shutil
import os
#Constants and variables initialization
lookup = '('
query = str()
output_query=[]
final_version=[]
################################################################
#Open up the file with the KLEE output
with open('KLEEout_raw.txt') as myFile:
        for line in myFile:
                if (line.startswith('KLEE:') | line.startswith('Current') | line.startswith('Using')):
                        continue
                else:
                        line = line.lstrip()
                        print line
                        output_query.append(line)
                        query = query + line

query = query.replace('\n(','(')
query = query.replace(')\n',')')
query = query.rstrip()
#For debugging purposes
#print ("------------------------------------------------")
#print (query)
################################################################
output_query = query.split('=:')
for item in output_query:
        if item.startswith('('):
                continue
        else:
                output_query.remove(item)
#For debugging purposes
#print ("------------------------------------------------")
#print (output_query)
################################################################

for item in output_query:
        if item.endswith(')'):
                final_version.append(item)
        else:
                print item
                final_version.append(re.sub(r'\)\w+$',')',item))
#For debugging purposes
#print (final_version)
################################################################

#Write the cleaned up data to a file
thefile = open('KLEEout_clean.txt', 'w')
for item in final_version:
  thefile.write("%s\n" % item)
thefile.close()
