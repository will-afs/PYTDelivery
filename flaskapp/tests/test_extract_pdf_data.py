import unittest
from pdfminer.pdfparser import PDFSyntaxError
from flaskapp.extract_pdf_data import extract_pdf_metadata

# tests settings
DATA_FILE_PATH = './flaskapp/resources/'
PDF_DATA_FILE_NAME = 'DOSSIER_COUP_DE_POUCE_2021.pdf'
NOT_EXISTING_DATA_FILE_NAME = 'file_name_which_does_not_exist'
NOT_PDF_DATA_FILE_NAME = 'dummy.text'

class TestExtractPDFData(unittest.TestCase):

    def test_extract_pdf_metadata_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_EXISTING_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_not_pdf(self):
        with self.assertRaises(PDFSyntaxError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_PDF_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_success(self):
        reference_metadata = {
                                'Author': b'AURORE',
                                'CreationDate': b"D:20200325185329+01'00'",
                                'Creator': b'Microsoft\xae Office Word 2007',
                                'ModDate': b"D:20210311153835+01'00'",
                                'Producer': b'Microsoft\xae Office Word 2007',
                                'Title': b'DOSSIER COUP DE POUCE 2020'
                            }
        extracted_metadata = extract_pdf_metadata(DATA_FILE_PATH + PDF_DATA_FILE_NAME)
        self.assertEqual(extracted_metadata, reference_metadata)