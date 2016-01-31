from database_builder import database_builder as dbb

#when pdf is uploaded directly
def extract_doi(filepath):
    #print("in extract doi with argument"+filepath)
    doi = dbb.process_and_add_one(filepath)
    return doi

def search_doi(doi):
    return query_citations_by_DOI(dbloc,doi)

def search_doi_by_title(title):
    return dbb.get_DOI_from_title(title)
