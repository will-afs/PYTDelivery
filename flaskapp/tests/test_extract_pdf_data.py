import unittest
from pdfminer.pdfparser import PDFSyntaxError
from flaskapp.core.extract_pdf_data import extract_pdf_metadata, extract_pdf_content

# tests settings
DATA_FILE_PATH = './flaskapp/tests/resources/'
PDF_DATA_FILE_NAME = 'PDF_FILE.pdf'
NOT_EXISTING_DATA_FILE_NAME = 'file_name_which_does_not_exist'
NOT_PDF_DATA_FILE_NAME = 'dummy.text'
PDF_CONTENT_REFERENCE = 'pdf_content_reference.txt'

class TestExtractPDFMetadata(unittest.TestCase):

    def test_extract_pdf_metadata_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_EXISTING_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_not_pdf(self):
        with self.assertRaises(PDFSyntaxError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_PDF_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_success(self):
        reference_metadata = {
                                'Author': 'AURORE',
                                'CreationDate': "D:20200325185329+01'00'",
                                'Creator': 'Microsoft Office Word 2007',
                                'ModDate': "D:20210311153835+01'00'",
                                'Producer': 'Microsoft Office Word 2007',
                                'Title': 'DOSSIER COUP DE POUCE 2020'
                            }
        extracted_metadata = extract_pdf_metadata(DATA_FILE_PATH + PDF_DATA_FILE_NAME)
        self.assertEqual(extracted_metadata, reference_metadata)


class TestExtractPDFContent(unittest.TestCase):

    def test_extract_pdf_content_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            extract_pdf_content(DATA_FILE_PATH + NOT_EXISTING_DATA_FILE_NAME)

    def test_extract_pdf_content_file_not_pdf(self):
        with self.assertRaises(PDFSyntaxError):
            extract_pdf_content(DATA_FILE_PATH + NOT_PDF_DATA_FILE_NAME)

    def test_extract_pdf_content_file_success(self):
        with open(DATA_FILE_PATH + PDF_CONTENT_REFERENCE, 'r') as pdf_content_reference_file:
            reference_content = pdf_content_reference_file.read()
        extracted_content = extract_pdf_content(DATA_FILE_PATH + PDF_DATA_FILE_NAME)
        self.assertEqual(extracted_content, reference_content)