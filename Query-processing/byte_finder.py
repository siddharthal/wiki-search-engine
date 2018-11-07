import json

fp = open('merged_index.txt','r')
fb = open('body.txt','w')
fc = open('cat.txt','w')
fi = open('info.txt','w')
fr = open('ref.txt','w')
fl = open('link.txt','w')
ft = open('title.txt','w')
fm = open('main_index.txt','w')
fa = open('bytearray.txt','w')

rval = 500
bytes = {}

while (1):
	try:
		line = fp.readline()
		pointer = fp.tell()
	except:
		break

	posting = line.split()
	try:
		term = posting.pop(0)
	except:
		# with open('bytes_dict.pkl','wb') as d:
		# 	json.dump(bytes,d)
		break

	body = []
	cat = []
	info = []
	ref = []
	link = []
	b = []
	c = []
	r = []
	l = []
	i = []
	t = []
	m = []

	for docs in posting:
		docid = ''
		bt,ct,rt,lt,it,tt = 0,0,0,0,0,0 
		bc = ''
		cc = ''
		rc = ''
		lc = ''
		ic = ''
		tc = ''

		for char in docs:
			if(char == 'b'):
				bt = 1
				ct,rt,lt,it,tt = 0,0,0,0,0
				continue

			if(char == 'c'):
				ct = 1
				bt,rt,lt,it,tt = 0,0,0,0,0
				continue
				
			if(char == 'r'):
				rt = 1
				ct,bt,lt,it,tt = 0,0,0,0,0
				continue
				
			if(char == 'l'):
				lt = 1
				ct,rt,bt,it,tt = 0,0,0,0,0
				continue
				
			if(char == 'i'):
				it = 1
				ct,rt,lt,bt,tt = 0,0,0,0,0
				continue
				
			if(char == 't'):
				tt = 1
				ct,rt,lt,it,bt = 0,0,0,0,0
				continue
				
			if (bt is 0 and ct is 0 and rt is 0 and lt is 0 and it is 0 and tt is 0 ):
				docid += char
			if(bt == 1):
				bc += char
			if(ct == 1):
				cc += char
			if(rt == 1):
				rc += char
			if(lt == 1):
				lc += char
			if(it == 1):
				ic += char
			if(tt == 1):
				tc += char
		mc = 0

		if(bc != ''):
			b.append([int(bc),docid])
			mc += int(bc)
		
		if(cc != ''):
			c.append([int(cc),docid])
			mc += int(cc)

		if(rc != ''):
			r.append([int(rc),docid])
			mc += int(rc)

		if(cc != ''):
			l.append([int(cc),docid])
			mc += int(cc)

		if(ic != ''):
			i.append([int(ic),docid])
			mc += int(ic)

		if(tc != ''):
			t.append([int(tc),docid])
			mc += int(tc)

		m.append([mc,docid])

	b.sort(key = lambda x:x[0],reverse=True)		
	c.sort(key = lambda x:x[0],reverse=True)		
	r.sort(key = lambda x:x[0],reverse=True)		
	l.sort(key = lambda x:x[0],reverse=True)		
	i.sort(key = lambda x:x[0],reverse=True)		
	t.sort(key = lambda x:x[0],reverse=True)		
	m.sort(key = lambda x:x[0],reverse=True)		


	a = ''

	if(len(b) != 0):
		poi = fb.tell()
		fb.write(term)
		a += '|'+ str(len(b)) + "-"+str(poi)
		b = b[:rval]
		for k in b:
			fb.write(" "+k[1]+"|"+str(k[0]))
		fb.write('\n')
	else:
		a += '|'

	if(len(c) != 0):
		poi = fc.tell()
		fb.write(term)
		a += '|'+ str(len(c)) + "-"+str(poi)		
		c = c[:rval]
		fc.write(term)
		for k in c:
			fc.write(" "+k[1]+"|"+str(k[0]))
		fc.write('\n')
	else:
		a += '|'

	if(len(r) != 0):
		poi = fr.tell()
		fr.write(term)
		a += '|'+ str(len(r)) + "-"+str(poi)
		r = r[:rval]
		for k in r:
			fr.write(" "+k[1]+"|"+str(k[0]))
		fr.write('\n')
	else:
		a += '|'
	
	if(len(l) != 0):
		poi = fl.tell()
		fl.write(term)
		a += '|'+str(len(l)) + "-"+ str(poi)
		l = l[:rval]
		for k in l:
			fl.write(" "+k[1]+"|"+str(k[0]))
		fl.write('\n')
	else:
		a += '|'
	
	if(len(i) != 0):
		poi = fi.tell()
		fi.write(term)
		a += '|'+str(len(i)) + "-"+ str(poi)
		i = i[:rval]
		for k in i:
			fi.write(" "+k[1]+"|"+str(k[0]))
		fi.write('\n')
	else:
		a += '|'
	
	if(len(t) != 0):	
		poi = ft.tell()
		ft.write(term)
		a += '|'+str(len(t)) + "-"+ str(poi)
		t = t[:rval]
		for k in t:
			ft.write(" "+k[1]+"|"+str(k[0]))
		ft.write('\n')
	else:
		a += '|'

	if(len(m) != 0):	
		poi = fm.tell()
		fm.write(term)
		a += '|'+ str(len(m)) + "-"+str(poi)
		m = m[:rval]
		for k in m:
			fm.write(" "+k[1]+"|"+str(k[0]))
		fm.write('\n')
	else:
		a += '|'

	fa.write(term + a + "\n")
	# bytes[term] = a

