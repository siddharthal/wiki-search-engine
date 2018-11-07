import os
import heapq

files_path = './index/'
files = os.listdir(files_path)

pointers = []

for i in files:
	pointers.append(open(files_path + i,'r'))

heap = []

for i in range(len(pointers)):
	heapq.heappush(heap,[pointers[i].readline(),i])

op = open('merged_index.txt','w')

while(len(heap) != 0):
	posting = heapq.heappop(heap)
	pointer = posting[1]
	try:
		posting = posting[0].split()
		term0 = posting.pop(0)

	except:
		continue

	term1 = term0[:]
	heapq.heappush(heap,[pointers[pointer].readline(),pointer])

	while (term1 == term0 and len(heap) != 0):
		posting1 = heapq.heappop(heap)
		pointer = posting1[1]
		try:
			posting_words = posting1[0].split()
			term1 = posting_words.pop(0)
		except:
			break

		if(term1 == term0):
			heapq.heappush(heap,[pointers[pointer].readline(),pointer])
			posting += posting_words
		else:
			heapq.heappush(heap, posting1)

	posting.sort()
	op.write(term0)
	for i in posting:
		op.write(' '+ i)
	op.write('\n')
