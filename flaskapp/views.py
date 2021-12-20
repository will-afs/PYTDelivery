import functools, json
from urllib.error import HTTPError
from flask import (
    Flask, Blueprint, g, request, make_response
)
from flaskapp.db.db import get_db, get_pdf_id, get_pdf, create_pdf, fill_pdf
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
                                "pdf_id":str(pdf_id),
                            }
            except PDFSyntaxError:
                status = 400
                data = {
                            "message":"The content pointed by the provided URI does not seem to be a PDF"
                        }                 
            except ValueError:
                status = 400
                data = {
                            "message":"Wrong URI format"
                        }
            except HTTPError:
                status = 400
                data = {
                            "message":"Could not access the provided URI"
                        }
            except Exception as err:
                status = 500
                data = {
                            "message":"Internal server error"
                        }
        else:
            status = 400
            data = {
                        "message":"Please provide an URI pointing to a file"
                    }
    else:
        status = 405
        data = {
                    "message":"Method now allowed"
                }
    response = make_response(data, status)
    return response


@bp.route('/documents/<int:pdf_id>/metadata.json/', methods=['GET'])
def get_pdf_metadata(pdf_id:int):
    """API endpoint to get PDF metadata from database, under json format

    Requires to specify the ID of the PDF in database
    """
    if request.method == 'GET':
        # Assuming at this step, routing has been done and thus <pdf_id> is not None
        if type(pdf_id) is int:
            pdf = get_pdf(get_db(), pdf_id)
            if pdf is None:
                status = 404
                data = {
                            "message":"No PDF with such ID in database"
                        }
            else:
                status = 200
                data = {
                            "message":"Successfully retrieved PDF metadata in database",
                            "metadata":pdf['metadata']
                        }
        else:
            status = 400
            data = {
                        "message":"Bad value for <pdf_id> in request URL. Expected a positive Integer",
                    }        
        response = make_response(data, status)
        return response

@bp.route('/documents/<int:pdf_id>/content.txt/', methods=['GET'])
def get_pdf_content(pdf_id:int):
    """API endpoint to get PDF content from database, as a .txt file

    Requires to specify the ID of the PDF in database
    """
    if request.method == 'GET':
        # Assuming at this step, routing has been done and thus <pdf_id> is not None
        if type(pdf_id) is int:
            pdf = get_pdf(get_db(), pdf_id)
            if pdf is None:
                status = 404
                data = {
                            "message":"No PDF with such ID in database"
                        }
            else:
                status = 200
                data = {
                            "message":"Successfully retrieved PDF content in database",
                            "content":pdf['content']
                        }
        else:
            status = 400
            data = {
                        "message":"Bad value for <pdf_id> in request URL. Expected a positive Integer",
                    }        
        response = make_response(data, status)
        return response