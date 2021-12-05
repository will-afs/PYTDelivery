from typing import List, Literal
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.high_level import extract_text
import urllib, os, glob
from pdfminer.pdfparser import PDFSyntaxError

TMP_DIRECTORY = './tmp'

def is_pdf(file_local_path:str)->bool:
    """Assuming the file being pointed by the URI exists, checks whether it is a PDF

    Parameters:
    file_local_path (str) : the path to access the local file

    Returns:
    bool: Whether the file is a PDF (True) or not (False)
    """
    is_pdf = True
    with open(file_local_path, 'rb') as pdf_file:
        try:
            PDFDocument(PDFParser(pdf_file)) # Should raise a PDFSyntaxError exception if not a real PDF
        except PDFSyntaxError:
            is_pdf = False
    return is_pdf

def clear_dir(dir_path:str=TMP_DIRECTORY):
    files = glob.glob(dir_path + '/*')
    for f in files:
        os.remove(f)

def download_pdf(file_uri:str, directory:str='./tmp') -> str:
    """Downloads a PDF acessible from a URI and stores it into the specified directory

    Parameters:
    file_uri (str) : the URI to access the file
    directory (str) : the directory into which saving the file

    Returns:
    str: The path to access the PDF saved locally
    """
    try:
        web_file = urllib.request.urlopen(file_uri)
    except urllib.error.HTTPError:
        raise FileNotFoundError('Could not access the provided URI')
    except ValueError:
        raise ValueError('Wrong URI format')
    else:
        file_name = file_uri.split('/')[-1]
        pdf_name = file_name.replace('.pdf', '') + '.pdf' # Delete eventual ".pdf" before adding it
        pdf_local_path = directory + '/' + pdf_name
        if not os.path.isfile(pdf_local_path):
            with open(pdf_local_path, 'wb') as pdf_file:
                pdf_file.write(web_file.read())
            web_file.close()
            if is_pdf(pdf_local_path):
                return pdf_local_path
            else:
                os.remove(pdf_local_path)
                raise PDFSyntaxError('The file being pointed by the provided URI does not seem to be a PDF')
        else:
            raise FileExistsError('File \"{}\" already exists'.format(pdf_name))   
        
def extract_pdf_metadata(pdf_path:str) -> dict:
    """Returns the metadata of a PDF

    Parameters:
    pdf_path (str) : the path of the PDF file of which metadata should be extracted

    Returns:
    dict: metadata of the PDF, presented as a JSON structured as follows : 
        {
            metadata:{
                        "Author": "AURORE",
                        "CreationDate": "D:20200325185329+01'00'",
                        "Creator": "Microsoft Office Word 2007",
                        "ModDate": "D:20210311153835+01'00'",
                        "Producer": "Microsoft Office Word 2007",
                        "Title": "DOSSIER COUP DE POUCE 2020"
                    }
            content:"Lorem ipsum dolor sit amet, ..."
        }
    """
    with open(pdf_path, 'rb') as pdf_file:
        pdf_parser = PDFParser(pdf_file)
        doc = PDFDocument(pdf_parser)
        metadata = doc.info[0]
        for (key, value) in doc.info[0].items():
            # Need to decode each value from bytestrings toward strings
            metadata[key] = value.decode("utf-8", errors='ignore')
        return metadata

def extract_pdf_content(pdf_path:str) -> str:
    """Returns the content of a PDF as a string

    Parameters:
    pdf_path (str) : the path of the PDF file of which content should be extracted

    Returns:
    str: content of the PDF as a string
    """
    with open(pdf_path,'rb') as pdf_file:
        content_as_string = extract_text(pdf_file)
        return content_as_string

def extract_pdf_data(pdf_uri:str) -> List:
    """Extracts PDF data acessible from a URI

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
    pdf_path = download_pdf(pdf_uri, TMP_DIRECTORY)
    pdf_metadata = extract_pdf_metadata(pdf_path)
    pdf_content = extract_pdf_content(pdf_path)
    clear_dir(TMP_DIRECTORY) # Remove the temporarily created file
    return pdf_metadata, pdf_content