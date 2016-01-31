from database_builder import database_builder as dbb

titledir = 'database_builder/titles'
bibsdir = 'database_builder/bibs'
dbloc = 'database_builder/master-db/master-db.json' 

#when pdf is uploaded directly
def extract_doi(filepath):
    doi = dbb.process_and_add_one(filepath,titledir,bibsdir,dbloc)
    return doi

def search_doi(doi):
    return 'akhdsafkdjsbf'

def search_doi_by_title(title):
    return dbb.get_DOI_from_title(title)
