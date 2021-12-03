import unittest
from flask import Flask
# from flaskapp.views import extract_pdf_metadata
import json

app = Flask(__name__)

PDF_DATA_FILE_NAME = 'PDF_FILE.pdf'
NOT_EXISTING_DATA_FILE_NAME = 'file_name_which_does_not_exist'
NOT_PDF_DATA_FILE_NAME = 'dummy.text'
EMPTY_FILE_NAME = None

# class TestExtractPDFData(unittest.TestCase):
#     def test_extract_pdf_metadata_success(self):
#         data_json = {
#                         'Author': 'AURORE',
#                         'CreationDate': "D:20200325185329+01'00'",
#                         'Creator': 'Microsoft Office Word 2007',
#                         'ModDate': "D:20210311153835+01'00'",
#                         'Producer': 'Microsoft Office Word 2007',
#                         'Title': 'DOSSIER COUP DE POUCE 2020',
#                     }
#         reference = {
#                         "data":json.dumps(data_json),
#                         "status_code":405
#                     }
#         urn = '/extract_pdf_metadata/' + PDF_DATA_FILE_NAME
#         with app.test_client() as client:
#             response = client.get(urn)
#             # received_json_data = response.get_json()
#             self.assertEqual(response.data, reference["data"])
#             self.assertEqual(response.status_code, reference["status_code"])
    
#     def test_extract_pdf_metadata_no_file_name_fails(self):
#         reference = {
#                         "data":'',
#                         "message":'',
#                         "status_code":400
#                     }
#         urn = '/extract_pdf_metadata/' + EMPTY_FILE_NAME
#         with app.test_client() as client:
#             response = client.get(urn)
#             self.assertEqual(response.data, reference["data"])
#             self.assertEqual(response.status_code, reference["status_code"])

#     def test_extract_pdf_metadata_wrong_file_name_fails(self):
#         reference = {
#                         "data":'',
#                         "message":'',
#                         "status_code":404
#                     }
#         urn = '/extract_pdf_metadata/' + NOT_EXISTING_DATA_FILE_NAME
#         with app.test_client() as client:
#             response = client.get(urn)
#             self.assertEqual(response.data, reference["data"])
#             self.assertEqual(response.status_code, reference["status_code"])
    
#     def test_extract_pdf_metadata_wrong_file_format_fails(self):
#         reference = {
#                         "data":'',
#                         "message":'',
#                         "status_code":405
#                     }
#         urn = '/extract_pdf_metadata/' + NOT_PDF_DATA_FILE_NAME
#         with app.test_client() as client:
#             response = client.get(urn)
#             self.assertEqual(response.data, reference["data"])
#             self.assertEqual(response.status_code, reference["status_code"])




# # @pytest.fixture
# def client():
#     db_fd, db_path = tempfile.mkstemp()
#     app = create_app({'TESTING': True, 'DATABASE': db_path})

#     with app.test_client() as client:
#         with app.app_context():
#             init_db()
#         yield client

#     os.close(db_fd)
#     os.unlink(db_path)