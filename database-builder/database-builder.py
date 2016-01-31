import os
import time
from tinydb import TinyDB, Query
import urllib2

db_loc = 'master-db/master-db.json'


#uses pdf-extract to get title of current paper
#source is source of pdf, destination is save location
def extract_title(source,dest):
        command = " ".join(["pdf-extract extract --titles", source,"--output",dest])
        
        if os.system(command)!= 0:
                print("Error in shell")
                f = open(dest,'a')
                f.write("title extraction failed")
                print "title extraction failed"
                return
        print "title extracted"
                
        
#source is source of pdf, destination is save location
def extract_bibtex(source,dest):
        command = " ".join(["pdf-extract extract-bib --resolved_references",source,"--output",dest])
        if os.system(command)!= 0:
                print("Error in shell")
                f = open(dest,'a')
                f.write("bibtex extraction failed")
                print "bibtext extraction failed"
                return 
        print "bibtex extracted"

def get_ref_list_DOIs(path):
        f = open(path,'r')
        bx = f.read()
        bx = bx.split('\n')
        DOIs =[]
        for line in bx:
                if 'url = ' in line:
                        a = line.split('{')
                        b = a[1].split('}')[0]
                        DOIs.append(b)
        return DOIs

def get_DOI_from_title(title):
        title = title.replace(' ','%20')
        print title
        lookup_string = "http://search.crossref.org/dois?q=" + title
        response = urllib2.urlopen(lookup_string)
        results = response.read()
        results = results.split('\n')
        for line in results:
                if '"doi": ' in line:
                        a = line.split('"')
                        return a[3]

def process_and_add_one(pdf_path,title_dir,bib_dir):
        pdf_name = pdf_path.split('/')
        pdf_name = pdf_name[-1]
        directory = pdf_path[0: -len(pdf_name)]
        stripped_name = pdf_name[0:-4]
        title_path = title_dir+"/"+stripped_name+".xml"
        extract_title(pdf_path,title_path)
        #check if title extraction worked, otherwise stop with this one
        tf = open(title_path, 'r')
        txml = tf.read()
        if txml == "title extraction failed":
                return


        #build dictionary with info we've got
        tf = open(title_path, 'r')
        txml = tf.read()
        txml = txml.split(">")
        title  = "title not found"
        for line in txml:
                if "</title" in line:
                        title = line[0:-7]
                        print title
                        break
                
                
        #save nice text version of title
        txt_name_path = title_path[0:-4]+".txt"
        ftxt = open(txt_name_path,'a')
        ftxt.write(title)
        if title == "title not found":
                return
        #if title was found, get DOI from it
        currDOI = get_DOI_from_title(title)
        #open/create tiny db
        db = TinyDB(db_loc)
        #make sure the paper isnt in the db already
        paper = Query()
        gotit = db.search(paper.ownDOI == currDOI)
        if gotit:
                return
        #only extract bibtex if you don't have it already, because this is the long part
        bib_path = bib_dir+"/"+stripped_name+".bib"
        extract_bibtex(pdf_path,bib_path)
        refDOIs = get_ref_list_DOIs(bib_path)
        
        new_dict = {"ownDOI":currDOI,"refDOIs":refDOIs}   
        db.insert(new_dict) 
     
               

        


        
def process_folder_of_pdfs(fpath):
        files = os.listdir(fpath)
        for line in files:
                path = fpath+"/"+ line
                print path
                process_and_add_one(path,'titles','bibs')


process_folder_of_pdfs('pdfs')

##extract_bibtex('pdfs/test1.pdf','bibs/test1.bib')
##extract_title('pdfs/test1.pdf','titles/test1title.xml')
##print get_DOI_from_title('Visualizing Document Content using Language Structure')   
        
##db = TinyDB('db.json')
##db.insert({'type': 'apple', 'count': 7})
##db.insert({'type': 'peach', 'count': 3})
##

            

#read the bibtex file

        


##
##def add_paper_to_db(db,source):
##    dest = 
    

            

            
