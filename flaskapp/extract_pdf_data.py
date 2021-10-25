from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

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
            metadata[key] = value.decode("utf-8", errors='ignore') # Need to decode bytestrings toward strings
        return metadata  # The "Info" metadata

if __name__ == "__main__":
    PDF_PATH = 'flaskapp/resources/DOSSIER_COUP_DE_POUCE_2021.pdf'
    print(extract_pdf_metadata(PDF_PATH))