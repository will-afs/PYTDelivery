import configparser
import json
import unittest


from flaskapp.core.extract_pdf_uris_from_atom_feed import extract_pdf_uris_from_atom_feed

config = configparser.ConfigParser()
TESTS_DIRECTORY = "./tests"
config.read(TESTS_DIRECTORY + "/setup.cfg")

DATA_FILE_PATH = config["PATHS"]["DATA_FILE_PATH"]
FEED_DATA_FILE_NAME = config["PATHS"]["FEED_DATA_FILE_NAME"]
REFERENCE_PDF_URIS_FILE_NAME = config["PATHS"]["REFERENCE_PDF_URIS_FILE_NAME"]


class TestExtractPDFURIsFromAtomFeed(unittest.TestCase):
    def test_extract_pdf_uris_from_atom_feed_success(self):
        with open(DATA_FILE_PATH + FEED_DATA_FILE_NAME, "rb") as feed_file:
            feed = feed_file.read()    
        pdf_uris = extract_pdf_uris_from_atom_feed(feed)
        with open(DATA_FILE_PATH + REFERENCE_PDF_URIS_FILE_NAME, "r") as reference_pdf_uris_file:
            reference_pdf_uris = [pdf_uri.replace('\n', '') for pdf_uri in reference_pdf_uris_file.readlines()] 
        self.assertEqual(pdf_uris, reference_pdf_uris)
    
    def test_extract_pdf_uris_from_not_not_bytesstring_fail(self):
        with self.assertRaises(TypeError):
            extract_pdf_uris_from_atom_feed(36)

    def test_extract_pdf_uris_from_empty_atom_feed_success(self):
        pdf_uris = extract_pdf_uris_from_atom_feed(b'svdfvdfv')
        self.assertEqual(pdf_uris, [])
