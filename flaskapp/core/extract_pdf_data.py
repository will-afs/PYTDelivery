from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.high_level import extract_text


def extract_pdf_metadata(pdf_path:str) -> dict:
    """Returns the metadata of a PDF

    Parameters:
    pdf_path (str) : the path of the PDF file of which metadata should be extracted

    Returns:
    dict: metadata of the PDF
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