from flask import (
    Flask, Blueprint, g, redirect, render_template, request, session, url_for, make_response
)
from flaskapp.db import get_db
from flaskapp.core import extract_pdf_data
from pdfminer.pdfparser import PDFSyntaxError
from werkzeug.utils import secure_filename

bp = Blueprint('core', __name__, url_prefix='/')


UPLOAD_FOLDER = './flaskapp/resources/'
ALLOWED_EXTENSIONS = {'pdf',}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(file_name:str) -> bool:
    """Returns whether a file is allowed for upload or not

    Parameters:
    file_name (str) : the name of the file

    Returns:
    bool: Whether the file is allowed for upload (True) or not (False)
    """
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload_local_pdf', methods=['POST'])
def upload_local_pdf():
    """API endpoint to upload a PDF stored locally on the client machine
    """
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if allowed_file(file.filename):
                file.save(dst = UPLOAD_FOLDER + secure_filename(file.filename))
                data = 'Uploaded file successfully'
                status = 200
            else:
                status = 405
                data = 'The file must be a PDF'
        else:
            status = 400
            data = 'Please provide a file'
        response = make_response(data, status)
        return response

@bp.route("/extract_pdf_metadata/<pdf_name>", methods=['GET'])
def extract_pdf_metadata(pdf_name):
    """API endpoint to extract PDF metadata
    """
    if request.method == 'GET':
        # pdf_name = request.args.get("pdf_name")
        pdf_path = UPLOAD_FOLDER + pdf_name
        try :
            data = extract_pdf_data.extract_pdf_metadata(pdf_path=pdf_path)
            status = 200
        except FileNotFoundError:
            data = "File not found"
            status = 404
        except PDFSyntaxError:
            data = "The file is not a PDF"
            status = 405    
        response = make_response(data, status)
        return response

@bp.route("/extract_pdf_content/<pdf_name>", methods=['GET'])
def extract_pdf_content(pdf_name):
    """API endpoint to extract PDF content
    """
    if request.method == 'GET':
        # pdf_name = request.args.get("pdf_name")
        pdf_path = UPLOAD_FOLDER + pdf_name
        try :
            data = extract_pdf_data.extract_pdf_content(pdf_path=pdf_path)
            status = 200
        except FileNotFoundError:
            data = "File not found"
            status = 404
        except PDFSyntaxError:
            data = "The file is not a PDF"
            status = 405
        response = make_response(data, status)
        return response