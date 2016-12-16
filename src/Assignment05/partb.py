import nltk
import nltk.chunk
import codecs
import viterbi
from collections import Counter
from sklearn.metrics import confusion_matrix
from nltk.corpus import conll2000

def load_sentences(path):
    sentences = []
    sentence = []
    for line in codecs.open(path, 'r', 'utf8'):
        line = line.rstrip()
        if not line:
            if len(sentence) > 0:
                if 'DOCSTART' not in sentence[0][0]:
                    sentences.append(sentence)
                sentence = []
        else:
            word = line.split()
            assert len(word) >= 2
            sentence.append(word)
    if len(sentence) > 0:
        if 'DOCSTART' not in sentence[0][0]:
            sentences.append(sentence)
    return sentences

train='./dataset/conll2000/train_lesser.txt'
allData=load_sentences(train)
globalData=[]
for i in allData:
    for j in i:
        globalData.append(j)

globalData=[tuple(l) for l in globalData]

freq_word=nltk.FreqDist(word for (word,tag,chunck) in globalData)
freq_tag=nltk.FreqDist(tag for (word,tag,chunck) in globalData)
freq_chunck=nltk.FreqDist(chunck for (word,tag,chunck) in globalData)  
allChunk=[a for a in freq_chunck]

allbigrams=list(nltk.bigrams(globalData))
alltrigrams=list(nltk.trigrams(globalData))

ch_type=[(a[2],b[2],c[2]) for (a,b,c) in alltrigrams]
dict1={i:ch_type.count(i) for i in set(ch_type)}

ch_type=[(a[2],b[2]) for (a,b) in allbigrams]
dict2={i:ch_type.count(i) for i in set(ch_type)}

#Probability of chunk being starting chunk
startchunk=dict(zip(allChunk,[1 for x in range(0,len(allChunk))]))
for i in allData:
    if i[0][2] in startchunk.keys():
        startchunk[i[0][2]]+=1
    else:
        startchunk[i[0][2]]=1
        
#Probability of chunk being ending chunk
endchunk=dict(zip(allChunk,[1 for x in range(0,len(allChunk))]))
for i in allData:
    if i[0][2] in endchunk.keys():
        endchunk[i[-1][2]]+=1
    else:
        endchunk[i[-1][2]]=1
        
result=[]
from collections import OrderedDict
sorted_startchunk = OrderedDict(reversed(sorted(startchunk.items(), key=operator.itemgetter(1))))
sorted_endchunk = OrderedDict(reversed(sorted(endchunk.items(), key=operator.itemgetter(1))))
sorted_x = OrderedDict(reversed(sorted(dict2.items(), key=operator.itemgetter(1))))
sorted_trigram= OrderedDict(reversed(sorted(dict1.items(), key=operator.itemgetter(1))))

result=result+[sorted_startchunk.items()[0][0]]
for (a,b) in sorted_x:
   if(a == sorted_startchunk.items()[0][0]) :
       result+= [b]
       break

prev=list(result)

for i in range(1,10) :
    for (a,b,c) in sorted_trigram:
       if(a == prev[0] and b == prev[1]) :
           result+= [c]
           prev.remove(a)
           prev=prev+[c]
           break
    
   
