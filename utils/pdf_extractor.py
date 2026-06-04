from pypdf import PdfReader

def pdf_file_c(pdf_file):

    re = PdfReader(pdf_file)
    pages = re.pages
    
    page_t = []
    for text in pages :
        extract = text.extract_text()
        page_t.append(extract)
    
    t = "\n ".join(page_t) 
    return t 






