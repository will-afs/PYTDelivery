import urllib
from io import BytesIO
from typing import List

from pdfminer.high_level import extract_text
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser, PDFSyntaxError


def get_file_object_from_uri(file_uri:str) -> BytesIO:
    """Return a Python File Object obtained from an URI

    Parameters:
    file_uri (str) : the URI to access the file

    Returns:
    io.BytesIO: File object corresponding to the file being pointed by the URI
    """
    try:
        response = urllib.request.urlopen(file_uri)
    except urllib.error.HTTPError:
        raise FileNotFoundError('Could not access the provided URI')
    except ValueError:
        raise ValueError('Wrong URI format')
    else:
        pdf_txt = response.read()
        file_object = BytesIO()
        file_object.write(pdf_txt)
        return file_object    

def extract_data_from_pdf_uri(pdf_uri:str) -> List:
    """Extracts data from a PDF being pointed by a URI

    Parameters:
    pdf_uri (str) : the URI through which access the file

    Returns:
    dict: metadata of the PDF, presented as a JSON structured as follows : 
        {
            "Producer": "GPL Ghostscript SVN PRE-RELEASE 8.62", 
            "CreationDate": "D:20080203020500-05'00'", 
            "ModDate": "D:20080203020500-05'00'", 
            "Creator": "dvips 5.499 Copyright 1986, 1993 Radical Eye Software",
            "Title": "dynamic.dvi"
        }
    str: PDF content
    """
    file_obj = get_file_object_from_uri(pdf_uri)
    pdf_parser = PDFParser(file_obj)
    doc = PDFDocument(pdf_parser)
    # 1. Extract PDF Metadata
    pdf_metadata = doc.info[0]
    for (key, value) in doc.info[0].items():
        # Need to decode each value from bytestrings toward strings
        pdf_metadata[key] = value.decode("utf-8", errors='ignore')
    # 2. Extract PDF content
    pdf_content = extract_text(file_obj)
    return pdf_metadata, pdf_content