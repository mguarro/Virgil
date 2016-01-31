import os
import time
from tinydb import TinyDB, Query
import urllib2
from lxml import etree


def query_citations_by_DOI(db_loc,DOI):
        db = TinyDB(db_loc)
        #make sure the paper isnt in the db already
        paper = Query()
        gotit = db.search(paper.ownDOI == DOI) #returns of list of dicts
        result_dict = gotit[0]
        if gotit:
                return result_dict['refDOIs']
        else:
                return None
        
#test code for query_ctations_by_DOI
#print query_citations_by_DOI('master-db/master-db.json','http://dx.doi.org/10.1109/tvcg.2014.2388208')

#uses pdf-extract to extract text (without refs) and saves as xml at dest and as
#txt with all the markup stripped in dest_txt
def extract_text(source,dest,dest_txt):
        command = " ".join(["pdf-extract extract --regions --no-linestles", source,"--output",dest])
        if os.system(command)!= 0:
                print("Error in shell")
                return False
        print "title extracted"
        tree = etree.parse(dest)
        notags = etree.tostring(tree,encoding = 'utf8',method ='text')
        f = open(dest_txt,'a')
        f.write(notags)
        print "text extracted"
        return True
#test code for extract_text:
#extract_text('pdfs/test.pdf','test_content.xml','text_content.txt')

#uses pdf-extract to get title of current paper
#source is source of pdf, destination is save location
def extract_title(source,dest):
        command = " ".join(["pdf-extract extract --titles", source,"--output",dest])
        
        if os.system(command)!= 0:
                print("Error in shell")
                f = open(dest,'a')
                f.write("title extraction failed")
                print "title extraction failed"
                return False
        print "title extracted"
        return True
                
        
#source is source of pdf, destination is save location
def extract_bibtex(source,dest):
        command = " ".join(["pdf-extract extract-bib --resolved_references",source,"--output",dest])
        print(command)
        if os.system(command)!= 0:
                print("Error in shell")
                f = open(dest,'a')
                f.write("bibtex extraction failed")
                print "bibtext extraction failed"
                return False
        print "bibtex extracted"
        return True

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
        return None

title_dir = 'database_builder/titles'
bib_dir = 'database_builder/bibs'
text_dir = 'database_builder/text'
db_loc = 'database_builder/master-db/master-db.json' 

def process_and_add_one(pdf_path):
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
                return None

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
                return None

        #if title was found, get DOI from it
        currDOI = get_DOI_from_title(title)
        #open/create tiny db
        db = TinyDB(db_loc)
        #make sure the paper isnt in the db already
        paper = Query()
        gotit = db.search(paper.ownDOI == currDOI)
        if gotit:
                return currDOI

        text_path_xml = text_dir +"/"+stripped_name+".xml"
        text_path_txt = text_dir + "/" +stripped_name+".txt"
        if not extract_text(pdf_path,text_path_xml,text_path_txt):
                print('text extraction failed')
                return None
                      
        #only extract bibtex if you don't have it already, because this is the long part
        #TODO: Return before doing bib extraction
        bib_path = bib_dir+"/"+stripped_name+".bib"
        if not extract_bibtex(pdf_path,bib_path):
            print("caught in the new code")
            return None

        refDOIs = get_ref_list_DOIs(bib_path)
        
        new_dict = {"ownDOI":currDOI,"refDOIs":refDOIs}   
        db.insert(new_dict)
        return currDOI 

#test code for process_and_add_one
#process_and_add_one('pdfs/test.pdf','titles','bibs','text','master-db/master-db.json')
               
def process_folder_of_pdfs(fpath,path_titles,path_bibs,path_text):
        files = os.listdir(fpath)
        for line in files:
                path = fpath+"/"+ line
                print path
                process_and_add_one(path,path_titles,path_bibs,path_text)


