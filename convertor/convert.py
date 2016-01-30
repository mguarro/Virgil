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
        

    #def getSections(self):
    #    os.system(        
