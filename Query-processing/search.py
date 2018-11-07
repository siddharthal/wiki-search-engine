import math
import time
import Stemmer
import re

fa = open('./bytearray.txt','r')
fb = open('./body.txt','r')
fc = open('./cat.txt','r')
fi = open('./info.txt','r')
fr = open('./ref.txt','r')
fl = open('./link.txt','r')
ft = open('./title.txt','r')
fm = open('./main_index.txt','r')
fd = open('./docs.txt','r')

di = {}
ndoc = float(17600000)
stemmer = Stemmer.Stemmer('english')


bytes = fa.readlines()
for line in bytes:
	k = line.split('|')
	key = k.pop(0)
	li = []
	if(len(di) % 1000000 is 0):
		print (len(di))
	for i in k:
		if(i == ''):
			li.append([])
			continue
		i = i.split('-')
		li.append([int(i[0]),int(i[1])])
	di[key] = li[:]

filedi = {}
try:
	while(1):
		byte = fd.tell()
		line = fd.readline()
		line = line.split()
		fre = line[len(line) -1 ].split('|')
		filedi[line.pop(0)] = [byte,int(fre[1])]
except:
	pass


k = 1.5
b = 0.75
davg = 418

top_hits = {}

def scorer(fp, q, pos):
    global top_hits
    print (q)
    q = re.sub(r'[^a-zA-Z0-9]+', ' ', q).lower().split()
    for word in q:        
        try:
            byte = di[stemmer.stemWord(word)][pos]
        except:
            continue
        
        fp.seek(byte[1])
        line = fp.readline()
        idf = math.log(byte[0]/ndoc)
        line = line.split()
        line.pop(0)
        for doc in line:
            d = doc.split('|')
            if(int(d[1]) is 0):
                continue
                
            if(d[0] in top_hits):
                top_hits[d[0]][1] += (1 + math.log(int(d[1]))) * idf
                top_hits[d[0]][0] += 1
            else:
                tf_idf = (1 + math.log(int(d[1]))) * idf
                top_hits[d[0]] = [1,tf_idf]
    
while(1):
    top_hits = {}
    print("Field|General(f|g)?")
    c = raw_input()
    if (c == 'g'):
        query = raw_input()
    else:
        print ("title:")
        ts = raw_input()
        print ("body:")
        bs = raw_input()
        print ("categories:")
        cs = raw_input()
        print ("infobox:")
        si = raw_input()
        print ("refernces:")
        rs = raw_input()
        print ("links:")
        ls = raw_input()
    
    start = time.time()
    if(c == 'f'):
        scorer(ft,ts,5)
        scorer(fb,bs,0)
        scorer(fc,cs,1)
        scorer(fr,rs,2)
        scorer(fl,ls,3)
        scorer(fi,si,4)        
        
    else:
        query = re.sub(r'[^a-zA-Z0-9]+', ' ', query).lower().split()
        for word in query:
            try:
                byte = di[stemmer.stemWord(word)][6]
            except:
                continue

            fm.seek(byte[1])
            line = fm.readline()
            idf = math.log((ndoc - byte[0] + 0.5)/(byte[0] + 0.5))
            line = line.split()
            line.pop(0)
            for doc in line:
                d = doc.split('|')
                if(int(d[1]) is 0):
                    continue
                doclen = filedi[d[0]][1]
                tf = 1 + (int(d[1])/float(doclen))
                okapi = (tf*(k+1)/(tf + k*((1 - b) + b*(doclen/davg))))
                score = okapi * idf

                if(d[0] in top_hits):
                    top_hits[d[0]][1] += score
                    top_hits[d[0]][0] += 1
                else:
                    tf_idf = score
                    top_hits[d[0]] = [1,tf_idf]
    
    results = top_hits.keys()
    results.sort(key = lambda x: (top_hits[x][0],top_hits[x][1]), reverse = True)
    
    for hit in results[:5000]: 
        title = ""
        fd.seek(filedi[hit][0])
        lin = fd.readline()
        lin = lin.split()
        for j in range(1,len(lin) -1 ):
            title += (lin[j] + " ")
        title += lin[len(lin) - 1].split('|')[0]
        title = title.lower().split()
        tl = len(title)
        q = query[:]
        for t in title:
            if t not in q:
                q.append(t)
        aub =  len(q)
        anb =  tl +  len(query) - len(q)
        trust = 1 + (anb/aub)
        top_hits[hit][1] *= trust
    
    results.sort(key = lambda x: (top_hits[x][0],top_hits[x][1]), reverse = True)

    for i in results[:10]:
        fd.seek(filedi[i][0])
        lin = fd.readline()
        lin = lin.split()
        str = ""
        for j in range(len(lin) -1 ):
            str += (lin[j] + " ")
        str += lin[len(lin) - 1].split('|')[0]
        print (str)
        print (top_hits[i][0])
    print "Time :", time.time() - start
