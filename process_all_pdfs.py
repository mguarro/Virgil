from database_builder import database_builder
from distance import distance
import os.path

cur_dir = os.path.dirname(__file__)
print "curr dir: "+ cur_dir
pdf_dir = cur_dir + "/database_builder/pdfs"
print pdf_dir
files = os.listdir(pdf_dir)
for line in files:
    pdf_path = pdf_dir+'/'+line
    print pdf_path
    DOI = database_builder.process_and_add_one(pdf_path)
    if DOI:
        distance.distance_add_new_DOI(DOI)
