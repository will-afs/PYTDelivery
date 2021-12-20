import functools, json

from flask import (
    Flask, Blueprint, g, request, make_response
)
from flaskapp.db.db import get_db
from flaskapp.db.pdf_utils import get_pdf_id, get_pdf, create_pdf, fill_pdf
from flaskapp.core.extract_pdf_data import extract_data_from_pdf_uri
from pdfminer.pdfparser import PDFSyntaxError
from werkzeug.utils import secure_filename

bp = Blueprint('core', __name__, url_prefix='/')


app = Flask(__name__)

@bp.route('/documents/', methods=['POST'])
def extract_pdf_metadata_and_content_from_uri():
    """API endpoint to extract metadata and content of a PDF accessible from a URI

    Requires to specify the URI of the PDF into the request parameters
    """
    if request.method == 'POST':
        if 'file_uri' in request.args:
            file_uri = request.args['file_uri']
            try:
                db = get_db()
                pdf_id = get_pdf_id(db, file_uri)
                if pdf_id is not None: # Check whether PDF matching URI already exists into DB
                    pdf = get_pdf(db, pdf_id)
                    status = 200
                    data = {
                                "message":"PDF matching the provided URI is already in base",
                                "pdf_id":str(pdf["id"]),
                            }
                else:
                    # Create new row for the PDF
                    pdf_id = create_pdf(db_cursor=db, file_uri=file_uri)
                    # TODO : launch a new task to asynchronously set row fields in db
                    metadata, content = extract_data_from_pdf_uri(file_uri)
                    metadata = json.dumps(metadata)
                    fill_pdf(db_cursor=db, pdf_id=pdf_id, metadata=metadata, content=content)
                    status = 200
                    data = {
                                "message":"Uploaded PDF successfully",
                                "pdf_id":pdf_id,
                            }                   
            except Exception as err:
                status = 400
                data = {
                            "message":err
                        }
        else:
            status = 400
            data = 'Please provide an URI pointing to a file '
    else:
        status = 405
        data = 'Method now allowed'
    response = make_response(data, status)
    return response

# @bp.route("/extract_pdf_metadata/<pdf_name>", methods=['GET'])
# def extract_pdf_metadata(pdf_name):
#     """API endpoint to extract PDF metadata
#     """
#     if request.method == 'GET':
#         # pdf_name = request.args.get("pdf_name")
#         pdf_path = UPLOAD_FOLDER + pdf_name
#         try :
#             data = extract_pdf_data.extract_pdf_metadata(pdf_path=pdf_path)
#             status = 200
#         except FileNotFoundError:
#             data = "File not found"
#             status = 404
#         except PDFSyntaxError:
#             data = "The file is not a PDF"
#             status = 405    
#         response = make_response(data, status)
#         return response

# @bp.route("/extract_pdf_content/<pdf_name>", methods=['GET'])
# def extract_pdf_content(pdf_name):
#     """API endpoint to extract PDF content
#     """
#     if request.method == 'GET':
#         # pdf_name = request.args.get("pdf_name")
#         pdf_path = UPLOAD_FOLDER + pdf_name
#         try :
#             data = extract_pdf_data.extract_pdf_content(pdf_path=pdf_path)
#             status = 200
#         except FileNotFoundError:
#             data = "File not found"
#             status = 404
#         except PDFSyntaxError:
#             data = "The file is not a PDF"
#             status = 405
#         response = make_response(data, status)
#         return response