#!/usr/bin/python

import sys
import re

input_file_name = "tweets.en.txt"
output_file_name = "Output.txt"
try:
  file = open(input_file_name, "r")
except IOError:
  print ("There was an error reading file")
  sys.exit()

try:
  ofile = open(output_file_name, "w")
except IOError:
  print ("There was an error reading file")
  sys.exit()
list_patterns = [
                r"(?:http?s?[\S]*)", #url
                r"\'ll |\'LL |\'re |\'RE |\'ve |\'VE |n\'t |N\'T ",
                r"\$?-?\d+[,[\d]+]*[\.[\d]+]?", #number     
                u"[@#\w\u00c0-\u00ff]+",  #words
                #u'\ud83c[\udf00-\udfff]', # U+1F300 to U+1F3FF
                #u'\ud83d[\udc00-\ude4f]', # U+1F400 to U+1F64F
                #u'\ud83d[\ude80-\udeff]'  # U+1F680 to U+1F6FF
                #u"[\uE000-\uF8FF]|\uD83C[\uDF00-\uDFFF]|\uD83D[\uDC00-\uDDFF]"
                #u"\u0001[\uF400-\uF64F]",
                u"[^@#\w\s\u00c0-\u00ff]+" #specialcharacter
                #r"[\S]+"
                ]
#count=1;
with file as f:
    for line in f:
           #print (line)	
           k = line.decode('utf-8')
           mylist = re.findall('|'.join(list_patterns),k)
           for item in mylist:
               ofile.write("<%s> " % item.encode('utf-8'))
           ofile.write("\n");         
file.close()
ofile.close()

