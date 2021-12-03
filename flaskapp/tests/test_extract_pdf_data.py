import unittest
from pdfminer.pdfparser import PDFSyntaxError
from flaskapp.core.extract_pdf_data import extract_pdf_metadata, extract_pdf_content
import configparser, json


config = configparser.ConfigParser()
config.read('./flaskapp/tests/test_extract_pdf_data.cfg')

DATA_FILE_PATH = config['PATHS']['DATA_FILE_PATH']
NOT_EXISTING_DATA_FILE_NAME = config['PATHS']['NOT_EXISTING_DATA_FILE_NAME']
NOT_PDF_DATA_FILE_NAME = config['PATHS']['NOT_PDF_DATA_FILE_NAME']
PDF_DATA_FILE_NAME = config['PATHS']['PDF_DATA_FILE_NAME']
PDF_CONTENT_REFERENCE = config['PATHS']['PDF_CONTENT_REFERENCE']
PDF_METADATA_REFERENCE = config['PATHS']['PDF_METADATA_REFERENCE']


class TestExtractPDFMetadata(unittest.TestCase):

    def test_extract_pdf_metadata_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_EXISTING_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_not_pdf(self):
        with self.assertRaises(PDFSyntaxError):
            extract_pdf_metadata(DATA_FILE_PATH + NOT_PDF_DATA_FILE_NAME)

    def test_extract_pdf_metadata_file_success(self):
        with open(DATA_FILE_PATH + PDF_METADATA_REFERENCE, 'r') as pdf_metadata_reference_file:
            reference_metadata = json.load(pdf_metadata_reference_file)
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