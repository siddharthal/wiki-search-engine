
# coding: utf-8

# In[1]:


import xml.sax
import re
from collections import Counter
import sys
import stopwords
import Stemmer

stemmer = Stemmer.Stemmer('english')
# In[2]:

index = {}

args = str(sys.argv)

class WikiParser( xml.sax.ContentHandler ):
    def __init__(self):
        self.current_tag = ''
        self.content = ''
        self.title =''
        self.revision = 0
        self.stopwords = stopwords.stopwords
        self.doc_count = 0

    # Call when an element starts
    def startElement(self, tag, attributes):
            
            if tag == "revision":
                self.revision = 1
            self.content = ''

   
    # Call when an elements ends
    def endElement(self, tag):
        if tag == "revision":
            self.revision = 0

        if tag =='text':
            self.parse_content(self.content)
        
        if tag =='title':
            self.title = self.content
            self.doc_count += 1

        if tag == 'id' and self.revision == 0:
            self.id = self.content
            

            
    def characters(self, content):
        self.content += content
    
    def parse_content(self,content):
        stack = ''
        text = ''
        references = ''
        infobox = ''
        categories = ''
        text_state = 1
        link_state = 0
        ref_state = 0
        info_state = 0
        cat_state = 0
        link = ''
        refer = ''
        refer_state = 0
        content = content.encode("utf-8")
        self.title = self.title.encode("utf-8")
        self.id = self.id.encode("utf-8")
        # print (self.id)
        forward = 0
        
        for char in range(len(content)):
            # print (forward)
            if(forward > 0):
                forward -= 1
                continue
            

            curr = int(char)
            try:                    
                stack += (content[char])

            except:
                continue

            if(content[char] == '<' and ref_state is 0):
                count = 1
                try:
                    t = 3
                    while(t):
                        t -=1
                        char += 1
                        stack += (content[char])
                        if(content[char] == '>'):
                            count -=1
                        elif (content[char] == '<'):
                            count += 1
                        if(stack[-4:] == '<ref' ):
                            count = 0
                    
                    while(count is not 0):
                        char += 1
                        stack += (content[char])
                        if(content[char] == '>'):
                            count -=1
                        elif (content[char] == '<'):
                            count += 1
                    forward = char - curr 
                    
                    if(stack[-4:] == '<ref' ):
                        while(content[char] != '>'):

                            char += 1
                            stack += (content[char])

                        forward = char - curr

                        if(stack[-2:] == '/>'):
                            continue
                        ref_state = 1
                        ref = ''
                        continue

                except:
                    continue

            try:

                if(stack[-4:] == 'http' ):
                    while(content[char] != ' '):
                        char += 1
                        stack += (content[char])

                    # if(ref_state is 1):
                    #     ref = ref[:-3]
                    # elif(text_state is 1):
                    #     text = text[:-3]

                    link += ' '
                    ref += ' '
                    text += ' '

                    forward = char - curr
                    continue

            except:
                continue
            
            if ref_state is 0: 
                try:
                    if (stack[-1*len('[[Category'):] == '[[Category'):
                        text_state = 0
                        info_state = 0
                        refer_state = 0
                        cat_state = 1
                        cat = ''
                        continue
                            

                except:
                    continue

            if cat_state is 1:
                cat += content[char]
                if(stack[-2:] == ']]'):
                    cat_state = 0
                    link_state = 0
                    categories += (cat + ' ')
                    text_state = 1
                continue
            
            if link_state is 1 and ref_state is 0:
                link += content[char]
                if(stack[-2:] == "=="):
                    link_state = 0
                    text_state = 1
                continue

            if refer_state is 1 and ref_state is 0:
                refer += content[char]
                if(stack[-2:] == "=="):
                    refer_state = 0
                    text_state = 1
                continue
                    
            if info_state is 1 and ref_state is 0:
                if(curl is not 0):
                    if (content[char] == '{'):
                        curl += 1
                    elif (content[char] == '}'):
                        curl -= 1
                    infobox += content[char]
                else:
                    text_state = 1
                    info_state = 0
                continue
                    
            if ref_state is 1:
                
                if(stack[-5:] != '/ref>'):
                    ref += content[char]
                    
                else:   
                    ref = ref[:-4]
                    references += (ref + ' ')
                    ref_state = 0
                continue
            if text_state is 1 and ref_state is  0:
                text += content[char]

            try:
                if(stack[-9] == '{' or stack[-9] == '='):
                    st = stack[-9:]

                    if (st == '{{Infobox'):
                        text_state = 0
                        info_state = 1
                        text += ' '
                        # text = text[:-9]
                        curl = 2
                        continue

                        

                    elif (st == '==Externa' or st == '== Extern'): 
                        text_state = 0
                        link_state = 1
                        link = ''
                        refer_state = 0
                        text += ' '
                        while(stack[-2:] != '=='):
                            char += 1
                            stack += (content[char])
                            forward = char - curr
                        continue 

                    elif (st == '==Referen' or st == '== Refere' or st == '===Cited ' or st == '=== Cited' or st == '==RefeBib' or st == '=Works cit'):
                        text_state = 0
                        refer_state = 1
                        text += ' '
                        refer = ''
                        while(stack[-2:] != '=='):
                            char += 1
                            stack += (content[char])
                            forward = char - curr
                        continue            
                
            except:
                continue

                    

        # print (text)
        # print (categories)
        # print (infobox)
        # print (categories)
        # print (link)
        
        self.indexer(text,(references +' '+ refer),link,categories,infobox)


    def stemmer(self,target):
        stripped = re.sub(r'[^a-zA-Z0-9]+', ' ', target).lower().split()
        # stripped = re.sub(r'\W+', ' ', target).lower().split()

        # stripped = re.sub(r'\W+', ' ', target).split()

        dummy = dict(Counter(stripped))
        bag = {}
        for token in dummy:
            if token not in self.stopwords:
                tok = stemmer.stemWord(token)
                if(tok not in bag):
                    bag[tok] = dummy[token]
                else:
                    bag[tok] += dummy[token]

        return bag

    # def inserter(self,target,field):
    #     global index
    #     for token in target:
    #         if(token not in index):
    #             index[token] = [[],[],[],[],[]]
    #         index[token][field].append([self.id,target[token]])

    def indexer(self,text,ref,link,categ,infobox):
        # print (self.title)
        global index
        title_bow = self.stemmer(re.sub('(?!^)([A-Z][a-z]+)', r' \1', self.title))
        text_bow = self.stemmer(text)
        ref_bow = self.stemmer(ref)
        link_bow = self.stemmer(link)
        categ_bow = self.stemmer(categ)
        infobox_bow = self.stemmer(infobox)
        strin = {}

        for key in title_bow:
            no = str(title_bow[key])
            strin[key] = (self.id +'t'+ str(title_bow[key]))
        for key in text_bow:
            if(key in strin):
                strin[key] += ('b' + str(text_bow[key]))
            else:
                strin[key] = (self.id +'b'+str(text_bow[key]))
        for key in ref_bow:
            if(key in strin):
                strin[key] += ('r' + str(ref_bow[key]))
            else:
                strin[key] = (self.id +'r'+str(ref_bow[key]))
        for key in link_bow:
            if(key in strin):
                strin[key] += ('l' + str(link_bow[key]))
            else:
                strin[key] = (self.id +'l'+str(link_bow[key]))
        for key in categ_bow:
            if(key in strin):
                strin[key] += ('c' + str(categ_bow[key]))
            else:
                strin[key] = (self.id +'c'+str(categ_bow[key]))
        for key in infobox_bow:
            if(key in strin):
                strin[key] += ('i' + str(infobox_bow[key]))
            else:
                strin[key] = (self.id + 'i'+str(infobox_bow[key]))

        for key in strin:
            if(key in index):
                index[key] += (' ' + strin[key])
            else:
                index[key] = (strin[key])
        # print (stri)
        # print (self.id)

        stri= ""
        # print (len(index))
        # for key in index:
        #     stri += (key + " " + index[key] + '\n')
        # self.inserter(title_bow,0)
        # self.inserter(text_bow,1)
        # self.inserter(ref_bow,2)
        # self.inserter(link_bow,3)
        # self.inserter(infobox_bow,4)




# In[3]:


if ( __name__ == "__main__"):
   
   # create an XMLReader
    parser = xml.sax.make_parser()
   # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
     
   # override the default ContextHandler
    Handler = WikiParser()
    parser.setContentHandler( Handler )
    parser.parse(sys.argv[1])
    sorted_keys = index.keys()
    sorted_keys.sort()
    stri= ""
    for key in sorted_keys:
        docs = index[key].split()
        docs.sort()
        stri += (key)
        for i in docs:
            stri += (" "+i)
        stri += '\n'
    op = open(sys.argv[2],"w")
    op.write(str(stri))
# In[ ]:




