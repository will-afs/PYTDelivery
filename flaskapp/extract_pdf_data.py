from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

def extract_pdf_metadata(pdf_path:str) -> dict:
    """Returns the metadata of a PDF

    Parameters:
    pdf_path (str) : the path of the PDF file of which metadata should be extracted

    Returns:
    dict: metadata of the PDF
    """
    with open(pdf_path, 'rb') as pdf_file: # If the file does not exist, raises the following error : FileNotFoundError
        # fp = open(, 'rb')
        pdf_parser = PDFParser(pdf_file) # If it is not a PDF, raises the following error : pdfminer.pdfparser.PDFSyntaxError
        doc = PDFDocument(pdf_parser)
        return doc.info[0]  # The "Info" metadata

if __name__ == "__main__":
    PDF_PATH = 'flaskapp/resources/dummy.text' # DOSSIER_COUP_DE_POUCE_2021.pdf
    print(extract_pdf_metadata(PDF_PATH))