import os
import time

class Convertor:

    '''
    Args:
    String: 'path/to/file/filename.pdf'
    
    Output: Text form of the pdf
    '''
    def __init__(self,filename):
        self.pdfpath = filename
        self.purename = os.path.basename(self.pdfpath).split(".")[0]
        self.textoutdir = 'converted-text/'
        self.xmloutdir = 'converted-xml/'

    #TODO: Timestamps to avoid filename clashes? 
    def getTextFilePath(self):
        self.outtext = self.textoutdir + self.purename +".txt"
        command = " ".join(["pdftotext ",self.pdfpath,self.outtext])
        if os.system(command) != 0:
            print("Error in shell")
        else:
            return os.path.abspath(self.outtext)

    #def getText(self):
    #    if os.path.exists():
 
    def getTitle(self):
        self.outtext = self.xmloutdir + self.purename + "-titles" +".xml"
        command = " ".join(["pdf-extract extract --titles",self.pdfpath,"--output",self.outtext])
        #print(command)
        if os.system(command) != 0:
            print("Error in shell")
        else:
            print("Result stored in: ",os.path.abspath(self.outtext))
            return os.path.abspath(self.outtext)

    def getReferences(self):
        self.outtext = self.xmloutdir + self.purename + "-references" +".xml"
        command = " ".join(["pdf-extract extract --references",self.pdfpath,"--output",self.outtext])
        if os.system(command) != 0:
            print("Error in shell")
        else:
            print("Result stored in: ",os.path.abspath(self.outtext))
            return os.path.abspath(self.outtext)

    def getResolvedReferences(self):
        self.outtext = self.xmloutdir + self.purename + "-resolved_references" +".xml"
        command = " ".join(["pdf-extract extract --resolved_references",self.pdfpath,"--output",self.outtext])
        if os.system(command) != 0:
            print("Error in shell")
        else:
            print("Result stored in: ",os.path.abspath(self.outtext))
            return os.path.abspath(self.outtext)

    def getRegions(self):
        self.outtext = self.xmloutdir + self.purename + "-regions" +".xml"
        command = " ".join(["pdf-extract extract --regions --no-lines",self.pdfpath,"--output",self.outtext])
        if os.system(command) != 0:
            print("Error in shell")
        else:
            print("Result stored in: ",os.path.abspath(self.outtext))
            return os.path.abspath(self.outtext)        

import sys

if __name__ == '__main__':
    c = Convertor(sys.argv[1])
    print(c.getTextFilePath())
