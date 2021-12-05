import unittest
from pdfminer.pdfparser import PDFSyntaxError
from flaskapp.core.extract_pdf_data import clear_dir, extract_pdf_metadata, extract_pdf_content, download_pdf, is_pdf, extract_pdf_data
import configparser, json, os, glob


config = configparser.ConfigParser()
TESTS_DIRECTORY = './tests'
config.read(TESTS_DIRECTORY + '/test_extract_pdf_data.cfg')

DATA_FILE_PATH = config['PATHS']['DATA_FILE_PATH']
NOT_EXISTING_DATA_FILE_NAME = config['PATHS']['NOT_EXISTING_DATA_FILE_NAME']
NOT_PDF_DATA_FILE_NAME = config['PATHS']['NOT_PDF_DATA_FILE_NAME']
PDF_DATA_FILE_NAME = config['PATHS']['PDF_DATA_FILE_NAME']
PDF_CONTENT_REFERENCE = config['PATHS']['PDF_CONTENT_REFERENCE']
PDF_METADATA_REFERENCE = config['PATHS']['PDF_METADATA_REFERENCE']
WRONG_PDF_URI = config['PATHS']['WRONG_PDF_URI']
NOT_FOUND_PDF_URI = config['PATHS']['NOT_FOUND_PDF_URI']
NOT_PDF_URI = config['PATHS']['NOT_PDF_URI']
PDF_URI = config['PATHS']['PDF_URI']
TMP_DIRECTORY = config['PATHS']['TMP_DIRECTORY']

class TestIsPDF(unittest.TestCase):

    def test_is_pdf_success(self):
        self.assertTrue(is_pdf(DATA_FILE_PATH+PDF_DATA_FILE_NAME))

    def test_is_pdf_fails(self):
        self.assertFalse(is_pdf(DATA_FILE_PATH+NOT_PDF_DATA_FILE_NAME))
    

class TestDownloadPDF(unittest.TestCase):
    def setUp(self) -> None:
        # Ensure there is no file in the folder before running these tests
        clear_dir(TMP_DIRECTORY)
        return super().setUp()

    def tearDown(self) -> None:
        # Ensure there is no file in the folder after running these tests
        clear_dir(TMP_DIRECTORY)
        return super().tearDown()

    def test_download_pdf_wrong_destionation_directory(self):
        with self.assertRaises(FileNotFoundError):
            download_pdf(PDF_URI, directory='----')

    def test_download_pdf_wrong_uri_format(self):
        with self.assertRaises(ValueError):
            download_pdf(WRONG_PDF_URI)

    def test_download_pdf_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            download_pdf(NOT_FOUND_PDF_URI)
    
    def test_download_pdf_file_not_pdf(self):
        with self.assertRaises(PDFSyntaxError):
            download_pdf(NOT_PDF_URI)

    def test_download_pdf_file_already_exists(self):
        download_pdf(PDF_URI)
        with self.assertRaises(FileExistsError):
            download_pdf(PDF_URI)

    def test_download_pdf_success(self):
        self.assertTrue(os.path.isfile(download_pdf(PDF_URI)))


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


class TestExtractPDFData(unittest.TestCase):

    def setUp(self) -> None:
        # Ensure there is no file in the folder before running these tests
        clear_dir(TMP_DIRECTORY)
        return super().setUp()

    def tearDown(self) -> None:
        # Ensure there is no file in the folder after running these tests
        clear_dir(TMP_DIRECTORY)
        return super().tearDown()

    def test_extract_pdf_data_success(self):
        extracted_metadata, extracted_content = extract_pdf_data(PDF_URI)
        # Checks metadata
        with open(DATA_FILE_PATH + PDF_METADATA_REFERENCE, 'r') as pdf_metadata_reference_file:
            reference_metadata = json.load(pdf_metadata_reference_file)
        self.assertEqual(extracted_metadata, reference_metadata)
        # Checks content
        with open(DATA_FILE_PATH + PDF_CONTENT_REFERENCE, 'r') as pdf_content_reference_file:
            reference_content = pdf_content_reference_file.read()
        self.assertEqual(extracted_content, reference_content)
        # Checks whether temporary PDF file has been successfuly deleted from tmp directory
        files = glob.glob(TMP_DIRECTORY + '/*')
        self.assertEqual(files, [])

    def test_extract_pdf_data_tmp_dir_does_not_exist_success(self):
        # Remove tmp directory
        if os.path.isdir(TMP_DIRECTORY):
            os.rmdir(TMP_DIRECTORY)

        self.test_extract_pdf_data_success()
        # Check that tmp folder has been created
        self.assertTrue(os.path.isdir(TMP_DIRECTORY))
